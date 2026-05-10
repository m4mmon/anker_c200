#!/usr/bin/env python3
"""
build_adb_patched_kernel_firmware.py
Build a modified Anker C200 firmware with:
  - ADB enabled (uvc.config + app_init.sh)
  - Kernel cmdline patched to expose ota_kernel partition (mtd4)

Usage: sudo python3 build_adb_patched_kernel_firmware.py firmware.img

Requirements:
    - mtd-utils (mkfs.jffs2):  sudo apt install mtd-utils
    - u-boot-tools (mkimage):  sudo apt install u-boot-tools
    - lzop:                    sudo apt install lzop
    - binwalk + jefferson:     pipx install jefferson
    - run as root
"""

import sys
import os
import re
import hashlib
import struct
import subprocess
import tempfile

JFFS2_OFFSET = 0x3F8080
JFFS2_SIZE   = 8388608
MTD1_OFFSET  = 0x80
MTD1_SIZE    = 0x3F8000
MKFS_JFFS2   = "/usr/sbin/mkfs.jffs2"

UVC_CONFIG_PATH = "config/uvc.config"
APP_INIT_PATH   = "init/app_init.sh"

ADB_ENABLE_PATCH = """\
# Enable ADB if disabled in persistent config
if grep -q "adb_en.*:0" /media/uvc.config 2>/dev/null; then
    sed -i "s/adb_en.*:0/adb_en          :1/" /media/uvc.config
fi
"""

OLD_CMDLINE = b'console=ttyS1,115200n8 mem=64M@0x0 rmem=64M@0x4000000 init=/linuxrc root=/dev/ram0 rw mtdparts=jz_sfc:32k(boot),4064k(kernel),8192k(appfs),256k(configfs) quiet'
NEW_CMDLINE = b'console=ttyS1,115200n8 mem=64M@0x0 rmem=64M@0x4000000 init=/linuxrc root=/dev/ram0 rw mtdparts=jz_sfc:32k(boot),4064k(kernel),8192k(appfs),256k(configfs),3840k(ota_kernel) quiet'


def verify_img(path):
    with open(path, 'rb') as f:
        data = f.read()
    magic = struct.unpack_from('<I', data, 0)[0]
    if magic != 0x7005:
        raise ValueError(f"Invalid magic: {magic:#010x} (expected 0x00007005)")
    content = data[0x80:]
    md5_header = data[0x0C:0x1C]
    md5_calc = hashlib.md5(content).digest()
    if md5_header != md5_calc:
        raise ValueError("MD5 mismatch")
    print(f"Input firmware OK: {len(data)} bytes, MD5 verified")
    return data


def get_real_user():
    real_user = os.environ.get("SUDO_USER")
    if not real_user:
        raise RuntimeError("SUDO_USER not set, please run with sudo")
    return real_user


def extract_jffs2(img_data, workdir):
    jffs2_data = img_data[JFFS2_OFFSET:JFFS2_OFFSET + JFFS2_SIZE]
    jffs2_path = os.path.join(workdir, "appfs.jffs2")
    with open(jffs2_path, 'wb') as f:
        f.write(jffs2_data)
    os.chmod(jffs2_path, 0o666)
    os.chmod(workdir, 0o777)

    extract_dir = os.path.join(workdir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    os.chmod(extract_dir, 0o777)

    real_user = get_real_user()
    subprocess.run(
        ["su", "-l", real_user, "-c", f"cd {extract_dir} && binwalk -eM {jffs2_path}"],
    )

    for root, dirs, files in os.walk(extract_dir):
        if "jffs2-root" in dirs:
            return os.path.join(root, "jffs2-root")

    raise RuntimeError("jffs2-root not found after extraction")


def patch_uvc_config(rootdir):
    path = os.path.join(rootdir, UVC_CONFIG_PATH)
    with open(path, 'r') as f:
        content = f.read()
    new_content = re.sub(r'adb_en\s*:0', 'adb_en          :1', content)
    if new_content == content:
        print(f"Warning: adb_en:0 not found in {UVC_CONFIG_PATH}, skipping")
        return
    with open(path, 'w') as f:
        f.write(new_content)
    print(f"Patched {UVC_CONFIG_PATH}: adb_en set to 1")


def patch_app_init(rootdir):
    path = os.path.join(rootdir, APP_INIT_PATH)
    with open(path, 'r') as f:
        content = f.read()
    if "Enable ADB if disabled" in content:
        print(f"{APP_INIT_PATH} already patched, skipping")
        return
    mount_line = "mount -t jffs2 /dev/mtdblock3 /media"
    if mount_line not in content:
        raise RuntimeError(f"Mount line not found in {APP_INIT_PATH}")
    content = content.replace(mount_line, mount_line + "\n" + ADB_ENABLE_PATCH)
    with open(path, 'w') as f:
        f.write(content)
    print(f"Patched {APP_INIT_PATH}: ADB activation script added")


def rebuild_jffs2(rootdir, workdir):
    output = os.path.join(workdir, "appfs_modified.jffs2")
    result = subprocess.run([
        MKFS_JFFS2,
        "--root", rootdir,
        "--eraseblock=0x8000",
        "--pagesize=0x1000",
        "--little-endian",
        "--output", output
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"mkfs.jffs2 failed: {result.stderr}")
    with open(output, 'rb') as f:
        data = f.read()
    data += bytes([0xFF]) * (JFFS2_SIZE - len(data))
    with open(output, 'wb') as f:
        f.write(data)
    print(f"JFFS2 rebuilt: {len(data)} bytes")
    return output


def patch_kernel(img_data, workdir):
    # Extraire le kernel uImage
    kernel_uimage = img_data[MTD1_OFFSET:MTD1_OFFSET + MTD1_SIZE]
    uimage_path = os.path.join(workdir, "kernel.uimage")
    with open(uimage_path, 'wb') as f:
        f.write(kernel_uimage)

    # Lire taille des données depuis header uImage (big-endian, offset 12)
    lzo_size = struct.unpack_from('>I', kernel_uimage, 12)[0]
    load_addr  = struct.unpack_from('>I', kernel_uimage, 16)[0]
    entry_point = struct.unpack_from('>I', kernel_uimage, 20)[0]
    print(f"Kernel: size={lzo_size}, load={load_addr:#010x}, ep={entry_point:#010x}")

    # Extraire données LZO
    lzo_path = os.path.join(workdir, "kernel.lzo")
    with open(lzo_path, 'wb') as f:
        f.write(kernel_uimage[64:64 + lzo_size])

    # Décompresser
    bin_path = os.path.join(workdir, "kernel.bin")
    subprocess.run(["lzop", "-d", "-f", "-o", bin_path, lzo_path])
    if not os.path.exists(bin_path):
        raise RuntimeError("lzop decompress failed")
    print(f"Kernel decompressed: {os.path.getsize(bin_path)} bytes")

    # Patcher cmdline
    with open(bin_path, 'rb') as f:
        data = bytearray(f.read())

    pos = data.find(OLD_CMDLINE)
    if pos < 0:
        raise RuntimeError("Cmdline not found in kernel")

    data[pos:pos + len(NEW_CMDLINE)] = NEW_CMDLINE
    data[pos + len(NEW_CMDLINE)] = 0
    print(f"Patched cmdline at {pos:#08x}: {len(OLD_CMDLINE)} -> {len(NEW_CMDLINE)} bytes")

    patched_bin_path = os.path.join(workdir, "kernel_patched.bin")
    with open(patched_bin_path, 'wb') as f:
        f.write(bytes(data))

    # Recompresser
    patched_lzo_path = os.path.join(workdir, "kernel_patched.lzo")
    result = subprocess.run(["lzop", "-9", "-f", "-o", patched_lzo_path, patched_bin_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"lzop compress failed: {result.stderr}")

    # Reconstruire uImage
    patched_uimage_path = os.path.join(workdir, "kernel_patched.uimage")
    result = subprocess.run([
        "mkimage", "-A", "mips", "-O", "linux", "-T", "kernel", "-C", "lzo",
        "-a", f"{load_addr:#010x}",
        "-e", f"{entry_point:#010x}",
        "-n", "Linux-3.10.14__isvp_swan_1.0__",
        "-d", patched_lzo_path,
        patched_uimage_path
    ]) #, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"mkimage failed: {result.stderr}")

    # Vérifier taille
    with open(patched_uimage_path, 'rb') as f:
        patched_uimage = f.read()

    if len(patched_uimage) > MTD1_SIZE:
        raise RuntimeError(f"Patched kernel too large: {len(patched_uimage)} > {MTD1_SIZE}")

    print(f"Kernel patched: {len(patched_uimage)} bytes (mtd1 max: {MTD1_SIZE})")

    # Padder à MTD1_SIZE
    return patched_uimage + bytes([0xFF]) * (MTD1_SIZE - len(patched_uimage))


def rebuild_img(kernel_padded, jffs2_path, output_path):
    with open(jffs2_path, 'rb') as f:
        appfs = f.read()
    content = kernel_padded + appfs
    md5 = hashlib.md5(content).digest()
    header = struct.pack('<I', 0x7005)
    header += struct.pack('<I', 0x8000)
    header += struct.pack('<I', len(content))
    header += md5
    header += bytes([0x00] * (128 - len(header)))
    final = header + content
    with open(output_path, 'wb') as f:
        f.write(final)
    print(f"Firmware rebuilt: {len(final)} bytes -> {output_path}")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: sudo {sys.argv[0]} firmware.img")
        sys.exit(1)

    if os.geteuid() != 0:
        print("Error: this script must be run as root")
        sys.exit(1)

    for tool, pkg in [(MKFS_JFFS2, "mtd-utils"), ("/usr/bin/lzop", "lzop"),
                      ("/usr/bin/mkimage", "u-boot-tools")]:
        if not os.path.exists(tool):
            print(f"Error: {tool} not found. Install with: sudo apt install {pkg}")
            sys.exit(1)

    input_path = sys.argv[1]
    output_path = os.path.splitext(input_path)[0] + "_adb_ota_kernel.img"

    print(f"\n=== 1. Verifying input firmware ===")
    try:
        img_data = verify_img(input_path)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as workdir:
        print(f"\n=== 2. Extracting JFFS2 filesystem ===")
        rootdir = extract_jffs2(img_data, workdir)
        print(f"Extracted to: {rootdir}")

        print(f"\n=== 3. Patching filesystem (ADB) ===")
        patch_uvc_config(rootdir)
        patch_app_init(rootdir)

        print(f"\n=== 4. Rebuilding JFFS2 ===")
        jffs2_path = rebuild_jffs2(rootdir, workdir)

        print(f"\n=== 5. Patching kernel cmdline ===")
        kernel_padded = patch_kernel(img_data, workdir)

        print(f"\n=== 6. Rebuilding firmware image ===")
        rebuild_img(kernel_padded, jffs2_path, output_path)

    print(f"\nDone. Modified firmware: {output_path}")
    print(f"Flash with: sudo python3 AnkerC200_flashtool.py {output_path}")


if __name__ == "__main__":
    main()
