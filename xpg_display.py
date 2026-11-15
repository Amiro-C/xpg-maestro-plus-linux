#!/usr/bin/env python3
import time
import usb.core
import usb.util
import psutil

VID = 0x125F
PID = 0x7601

def get_cpu_temp():
    temps = psutil.sensors_temperatures()
    for name in ('k10temp', 'coretemp', 'zenpower', 'acpitz'):
        sensor_list = temps.get(name)
        if sensor_list:
            for entry in sensor_list:
                if entry.label in ('Tctl', 'Package id 0', 'Tdie', ''):
                    return int(round(entry.current))
            return int(round(next(iter(sensor_list)).current))
    return 0

def get_ram_usage():
    return int(round(psutil.virtual_memory().percent))

def get_cpu_usage():
    return int(round(psutil.cpu_percent(interval=None)))

def clamp_byte(val, max_val=100):
    return max(0, min(max_val, int(val)))

def build_payload(cpu_temp, ram_pct, cpu_pct):
    header = bytes([
        0x07,                      # byte_0: Report ID
        0xA1,                      # byte_1: Command / Subtype Magic
        0x01,                      # byte_2: Mode / Version Flag
        0x00, 0x00, 0x00,          # bytes_3_5: Reserved Padding
        0x0A,                      # byte_6: Telemetry Marker 1
        clamp_byte(cpu_temp, 255), # byte_7: CPU TEMP
        0x0A,                      # byte_8: Telemetry Marker 2
        clamp_byte(ram_pct, 100),  # byte_9: RAM USAGE
        clamp_byte(cpu_pct, 100),  # byte_10: CPU USAGE
        0x07, 0x07, 0x07           # bytes_11_13: Status Flags
    ])
    return header + bytes(64 - len(header))

def main():
    psutil.cpu_percent(interval=None)
    
    while True:
        dev = None
        try:
            dev = usb.core.find(idVendor=VID, idProduct=PID)
            if dev is None:
                raise RuntimeError("Device 125f:7601 not found")

            if dev.is_kernel_driver_active(0):
                dev.detach_kernel_driver(0)

            usb.util.claim_interface(dev, 0)
            print("Connected to XPG MAESTRO PLUS 62DA")

            while True:
                temp = get_cpu_temp()
                ram = get_ram_usage()
                cpu = get_cpu_usage()
                
                packet = build_payload(temp, ram, cpu)
                sent = dev.ctrl_transfer(0x21, 0x09, 0x0207, 0x0000, packet)
                
                if sent != 64:
                    raise RuntimeError(f"Incomplete transfer: {sent} bytes")

                time.sleep(1.0)

        except Exception as e:
            print(f"Error: {e}. Retrying in 5s...")
            time.sleep(5)
        finally:
            if dev is not None:
                try:
                    usb.util.release_interface(dev, 0)
                except Exception:
                    pass

if __name__ == "__main__":
    main()
