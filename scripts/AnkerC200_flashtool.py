#!/usr/bin/env python3
"""
Anker PowerConf C200 firmware flash tool
Usage: sudo python3 AnkerC200_flashtool.py firmware.img
"""

import sys
import os
import time
import struct
import hashlib
import glob
import usb.core
import usb.util
import serial

VID = 0x291a
PID = 0x3369
FRAME_PAYLOAD_SIZE = 498
FRAME_TOTAL_SIZE   = 512
BATCH_SIZE         = 2000


def checksum(data):
    return sum(data) & 0xff


def verify_img(path):
    """Check .img magic and md5"""
    with open(path, 'rb') as f:
        data = f.read()
    magic = struct.unpack_from('<I', data, 0)[0]
    if magic != 0x7005:
        raise ValueError(f"Invalid Magic: {magic:#010x} (expected 0x00007005)")
    content = data[0x80:]
    md5_header = data[0x0C:0x1C]
    md5_calc = hashlib.md5(content).digest()
    if md5_header != md5_calc:
        raise ValueError(f"Invalid MD5: {md5_calc.hex()} != {md5_header.hex()}")
    print(f"Firmware OK: {len(data)} bytes, MD5 checked")
    return data


def build_init_cmd(firmware_size):
    frame_count = (firmware_size + FRAME_PAYLOAD_SIZE - 1) // FRAME_PAYLOAD_SIZE
    cmd = bytearray([
        0x08, 0xEE, 0x00, 0x00, 0x00, 0x07, 0x01, 0x1A,
        0x00, 0x00, 0x05, 0xF2, 0x01
    ])
    cmd += struct.pack('<I', firmware_size)
    cmd += struct.pack('<H', frame_count)
    cmd += bytes([0x00, 0x00, 0x00, 0x00])
    cmd += struct.pack('<H', BATCH_SIZE)
    cmd += bytes([checksum(cmd)])
    return bytes(cmd)


def build_data_frame(data_chunk, frame_idx):
    header = bytes([0x08, 0xEE, 0x00, 0x00, 0x00, 0x07, 0x03])
    length = struct.pack('<H', FRAME_TOTAL_SIZE)
    index  = struct.pack('<I', frame_idx)
    frame  = header + length + index + data_chunk
    return frame + bytes([checksum(frame)])


def list_serial_devs():
    return set(glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*'))


def connect_camera():
    dev = usb.core.find(idVendor=VID, idProduct=PID)
    if not dev:
        raise RuntimeError(f"Camera not found (VID={VID:#06x} PID={PID:#06x})")
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    return dev


def read_version(dev):
    r = dev.ctrl_transfer(0xa1, 0x81, 0x0c00, 0x0600, 60, timeout=5000)
    return bytes(r).split(b'\x00')[0].decode('ascii', errors='replace')


def trigger_cdc(dev):
    payload = bytes([0x06, 0x01]) + b'\x00' * 58
    dev.ctrl_transfer(0x21, 0x01, 0x0d00, 0x0600, payload, timeout=5000)
    usb.util.dispose_resources(dev)


def wait_cdc_port(ports_before, timeout=15):
    for _ in range(timeout * 2):
        time.sleep(0.5)
        new = list_serial_devs() - ports_before
        if new:
            return new.pop()
    raise RuntimeError("CDC port did not spawn")


def send_firmware(port, firmware):
    size = len(firmware)
    frame_count = (size + FRAME_PAYLOAD_SIZE - 1) // FRAME_PAYLOAD_SIZE

    ser = serial.Serial(port=port, baudrate=115200, timeout=10)
    time.sleep(0.5)

    # Init
    init_cmd = build_init_cmd(size)
    print(f"Sending init request: {init_cmd.hex(' ').upper()}")
    ser.write(init_cmd)
    resp = ser.read(14)
    print(f"Response            : {resp.hex(' ').upper()}")
    if not resp or resp[1] != 0xFF:
        raise RuntimeError(f"Init failed: {resp.hex()}")
    print("Init OK\n")

    # Frames
    sent = 0
    frame_idx = 0
    while sent < size:
        chunk = firmware[sent:sent + FRAME_PAYLOAD_SIZE]
        if len(chunk) < FRAME_PAYLOAD_SIZE:
            chunk = chunk + bytes(FRAME_PAYLOAD_SIZE - len(chunk))
        ser.write(build_data_frame(chunk, frame_idx))
        sent = min(sent + FRAME_PAYLOAD_SIZE, size)
        frame_idx += 1
        print(f"\r  {frame_idx / frame_count * 100:.0f}% — frame {frame_idx}/{frame_count}", end='', flush=True)
        if frame_idx % BATCH_SIZE == 0:
            ack = ser.read(14)
            idx_ack = struct.unpack_from('<I', ack, 9)[0] if ack and len(ack) >= 13 else -1
            print(f"\n  ACK index={idx_ack}")

    print(f"Sending firmware done ({frame_idx} frames)")

    # ACK final
    print("Waiting for final ACK...")
    final = ser.read(12)
    print(f"Final ACK: {final.hex(' ').upper() if final else 'rien'}")
    if final and len(final) >= 7 and final[6] == 0x05:
        print("Camera has successfully checked the data")
    else:
        print("WARNING: waiting final ACK")

    ser.close()


def main():
    if len(sys.argv) != 2:
        print(f"Usage: sudo {sys.argv[0]} firmware.img")
        sys.exit(1)

    firmware_path = sys.argv[1]
    if not os.path.exists(firmware_path):
        print(f"File not found: {firmware_path}")
        sys.exit(1)

    # 1. check firmware
    print(f"\n=== 1. Checking firmware: {firmware_path} ===")
    try:
        firmware = verify_img(firmware_path)
    except ValueError as e:
	    print(f"Error: {e}")
	    sys.exit(1)

    # 2. Detect camera
    print("\n=== 2. Detecting camera ===")
    try:
        dev = connect_camera()
    except RuntimeError as e:
	    print(f"Error: {e}")
	    sys.exit(1)
    print("Camera found")

    # 3. Reading version
    try:
        version = read_version(dev)
    except usb.core.USBError as e:
        print(f"Error: could not read version: {e}")
        sys.exit(1)
    print(f"Current camera firmware version: {version}")

    # 4. Switch to CDC mode
    print("\n=== 4. Request camera to switch t CDC mode ===")
    ports_before = list_serial_devs()
    print(f"Serial ports before: {ports_before}")
    trigger_cdc(dev)
    print("Command sent, waiting for CDC port...")
    port = wait_cdc_port(ports_before)
    print(f"Port detected: {port}")

    # 5. Send firmware
    print(f"\n=== 5. Sending firmware ({len(firmware)} bytes) ===")
    send_firmware(port, firmware)

    # 6. done
    print("Done. Wait a few minutes, the camera should reboot itself and become available again.")


if __name__ == "__main__":
    main()
