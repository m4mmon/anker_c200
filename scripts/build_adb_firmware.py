#!/usr/bin/env python3
"""
build_adb_firmware.py - Build a modified Anker C200 firmware with ADB enabled

Usage: python3 build_adb_firmware.py Kiva_anker_update_package_c200_7.5_230423171038.img

Requirements:
    - mtd-utils package (mkfs.jffs2): sudo apt install mtd-utils
    - run as root (mkfs.jffs2 requires it)

What this script does:
    1. Extracts the JFFS2 filesystem from the original firmware
    2. Modifies config/uvc.config to enable ADB by default
    3. Modifies init/app_init.sh to force ADB activation on boot,
       even on cameras that have been previously used with ADB disabled
    4. Rebuilds the JFFS2 filesystem and the firmware image
"""

import hashlib
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

JFFS2_OFFSET = 0x3F8080
JFFS2_SIZE   = 8388608
MKFS_JFFS2   = "/usr/sbin/mkfs.jffs2"

UVC_CONFIG_PATH = "config/uvc.config"
APP_INIT_PATH   = "init/app_init.sh"

ADB_ENABLE_PATCH = """\
# Enable ADB if disabled in persistent config
if grep -q "adb_en.*:0" /media/uvc.config 2>/dev/null; then
    sed -i "s/adb_en.*:0/adb_en          :1/" /media/uvc.config
fi
"""


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
        raise ValueError(f"MD5 mismatch")
    print(f"Input firmware OK: {len(data)} bytes, MD5 verified")
    return data


def extract_jffs2_XXX(img_data, workdir):
    """Extracts JFFS2 content using binwalk"""
    jffs2_data = img_data[JFFS2_OFFSET:JFFS2_OFFSET + JFFS2_SIZE]
    jffs2_path = os.path.join(workdir, "appfs.jffs2")
    with open(jffs2_path, 'wb') as f:
        f.write(jffs2_data)

    # Extract with binwalk
    extract_dir = os.path.join(workdir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    result = subprocess.run(
        ["binwalk", "--run-as=root", "--extract", "--directory", extract_dir, jffs2_path],
        capture_output=True, text=True
    )
    print(f"Extraction directory contents:")
    for root, dirs, files in os.walk(extract_dir):
        print(f"  {root}: dirs={dirs} files={files[:3]}")
    if result.returncode != 0:
        raise RuntimeError(f"binwalk failed: {result.stderr}")

    # Find jffs2-root
    for root, dirs, files in os.walk(extract_dir):
        if "jffs2-root" in dirs:
            return os.path.join(root, "jffs2-root")

    raise RuntimeError("jffs2-root not found after extraction")


def extract_jffs2_YYY(img_data, workdir):
    jffs2_data = img_data[JFFS2_OFFSET:JFFS2_OFFSET + JFFS2_SIZE]
    jffs2_path = os.path.join(workdir, "appfs.jffs2")
    with open(jffs2_path, 'wb') as f:
        f.write(jffs2_data)

    rootdir = os.path.join(workdir, "jffs2-root")
    os.makedirs(rootdir, exist_ok=True)

    result = subprocess.run(
        ["jefferson", "-d", rootdir, jffs2_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"jefferson failed: {result.stderr}")

    return rootdir


def extract_jffs2(img_data, workdir):
    jffs2_data = img_data[JFFS2_OFFSET:JFFS2_OFFSET + JFFS2_SIZE]
    jffs2_path = os.path.join(workdir, "appfs.jffs2")
    with open(jffs2_path, 'wb') as f:
        f.write(jffs2_data)
    extract_dir = os.path.join(workdir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    os.chmod(jffs2_path, 0o666)
    os.chmod(workdir, 0o777)
    os.chmod(extract_dir, 0o777)

    real_user = os.environ.get("SUDO_USER")
    if not real_user:
        raise RuntimeError("SUDO_USER not set, please run with sudo")

    result = subprocess.run(
        ["su", "-l", real_user, "-c", f"cd {extract_dir} && binwalk -eM {jffs2_path}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"binwalk failed: {result.stderr}")

    print(f"Extraction directory contents:")
    for root, dirs, files in os.walk(extract_dir):
        print(f"  {root}: dirs={dirs} files={files[:3]}")

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

    # Insert after the mount line
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

    # Pad to JFFS2_SIZE with 0xFF
    with open(output, 'rb') as f:
        data = f.read()
    data += bytes([0xFF]) * (JFFS2_SIZE - len(data))
    with open(output, 'wb') as f:
        f.write(data)
    print(f"JFFS2 rebuilt: {len(data)} bytes")
    return output


def rebuild_img(original_data, jffs2_path, output_path):
    kernel = original_data[0x80:JFFS2_OFFSET]
    with open(jffs2_path, 'rb') as f:
        appfs = f.read()
    content = kernel + appfs
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
        print("Error: this script must be run as root (required for mkfs.jffs2)")
        sys.exit(1)

    if not os.path.exists(MKFS_JFFS2):
        print(f"Error: {MKFS_JFFS2} not found. Install mtd-utils: sudo apt install mtd-utils")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = os.path.splitext(input_path)[0] + "_adb.img"

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

        print(f"\n=== 3. Patching filesystem ===")
        patch_uvc_config(rootdir)
        patch_app_init(rootdir)

        print(f"\n=== 4. Rebuilding JFFS2 ===")
        jffs2_path = rebuild_jffs2(rootdir, workdir)

        print(f"\n=== 5. Rebuilding firmware image ===")
        rebuild_img(img_data, jffs2_path, output_path)

    print(f"\nDone. Modified firmware: {output_path}")
    print(f"Flash with: sudo python3 AnkerC200_flashtool.py {output_path}")


if __name__ == "__main__":
    main()
