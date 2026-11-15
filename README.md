# XPG Maestro Plus 62DA Linux Driver

Open-source user-space USB HID driver for the **Adata XPG Maestro Plus 62DA** CPU cooler segment display on Linux.

Reverse-engineered via USB packet capture (`VID: 0x125f`, `PID: 0x7601`), this lightweight Python daemon reads real-time system telemetry (`CPU Temperature`, `RAM Usage`, and `CPU Usage`) and pushes 64-byte HID `SET_REPORT` control transfers to the display controller (`HWCX`) every second.


## Features
* Displays **CPU Temperature** (°C)
* Displays **RAM Usage** (%)
* Displays **CPU Usage** (%)
* Automatic USB reconnection handling
* Systemd user service integration
* Zero root privileges required at runtime (via `udev` rules)

## Hardware Support
* **Cooler:** Adata XPG Maestro Plus 62DA
* **USB Vendor ID:** `0x125f` (A-DATA Technology Co., Ltd.)
* **USB Product ID:** `0x7601` (HWCX XPG MAESTRO PLUS 62DA)

## Requirements
* Python 3.8+
* `pyusb` (`python-pyusb`)
* `psutil` (`python-psutil`)

### Installing dependencies
* **Arch Linux / Manjaro:**
  ```bash
  sudo pacman -S python-pyusb python-psutil
  ```
* **Debian / Ubuntu / Linux Mint:**
  ```bash
  sudo apt install python3-usb python3-psutil
  ```
* **Fedora:**
  ```bash
  sudo dnf install python3-pyusb python3-psutil
  ```

## Quick Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Amiro-C/xpg-maestro-plus-linux
   cd xpg-maestro-plus-linux
   ```
2. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
### Arch Linux / Manjaro (via PKGBUILD)

1. Clone the repository and build the package:
   ```bash
   git clone https://github.com/Amiro-C/xpg-maestro-plus-linux
   cd xpg-maestro-plus-linux
   makepkg -si
   ```
2. Reload udev rules and enable the user service:
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   systemctl --user enable --now xpg-display.service
   ```

## USB HID Protocol Specification

The controller communicates over Interface `0` using USB HID `SET_REPORT` control transfers (`bmRequestType: 0x21`, `bRequest: 0x09`, `wValue: 0x0207`, `wIndex: 0x0000`) with a 64-byte payload updated at 1 Hz:

| Byte Offset | Value / Type | Description |
| :--- | :--- | :--- |
| `0` | `0x07` | HID Report ID |
| `1` | `0xA1` | Command / Subtype Magic |
| `2` | `0x01` | Mode / Version Flag |
| `3..5` | `0x00` | Reserved Padding |
| `6` | `0x0A` | Telemetry Marker 1 |
| `7` | `0x00–0xFF` | **CPU Temperature** (°C) |
| `8` | `0x0A` | Telemetry Marker 2 |
| `9` | `0x00–0x64` | **RAM Usage** (%) |
| `10` | `0x00–0x64` | **CPU Usage** (%) |
| `11..13` | `0x07` | Status Flags |
| `14..63` | `0x00` | Zero Padding |

## License
MIT License
