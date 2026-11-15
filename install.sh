#!/usr/bin/env bash
set -e

echo "Installing XPG Maestro Plus 62DA driver..."

mkdir -p ~/.local/bin
cp xpg_display.py ~/.local/bin/xpg_display.py
chmod +x ~/.local/bin/xpg_display.py

echo "Installing udev rules (requires sudo)..."
sudo cp 99-xpg-maestro.rules /etc/udev/rules.d/99-xpg-maestro.rules
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Enabling systemd user service..."
mkdir -p ~/.config/systemd/user
cp xpg-display.service ~/.config/systemd/user/xpg-display.service
systemctl --user daemon-reload
systemctl --user enable --now xpg-display.service

echo "Installation complete! Service status:"
systemctl --user status xpg-display.service --no-pager
