#!/usr/bin/env bash

sudo groupadd -r autologin
sudo gpasswd -a $USER autologin

# To autologin to the Xubuntu Desktop X Server
if [ -f "/etc/lightdm/lightdm.conf" ]; then
    sudo rm "/etc/lightdm/lightdm.conf"
fi
sudo ln -s $HOME/grand-prix/.xubuntu/lightdm.conf \
  /etc/lightdm/lightdm.conf

# To launch MPF after starting the X Server
if [ -f "$HOME/.config/autostart/mpf.desktop" ]; then
    rm "$HOME/.config/autostart/mpf.desktop"
fi
mkdir -p $HOME/.config/autostart
ln -s $HOME/grand-prix/.xubuntu/mpf.desktop \
  $HOME/.config/autostart/mpf.desktop

# Prevents a serial error with some hardware
sudo usermod -a -G dialout $USER
# Probably prevents full minute delay when not
# connected to the internet (unconfirmed)
sudo sed -i -e 's/NM_ONLINE_TIMEOUT=60/NM_ONLINE_TIMEOUT=5/g' \
  /etc/systemd/system/network-online.target.wants/NetworkManager-wait-online.service

# Remap Caps Lock to Backspace for VIM
sudo sed -i -e 's/XKBOPTIONS=\"\"/XKBOPTIONS=\"caps:backspace\"/g' /etc/default/keyboard
sudo dpkg-reconfigure keyboard-configuration

# Alias serial devices
[ -e "/etc/udev/rules.d/opp.rules" ] && sudo rm "/etc/udev/rules.d/opp.rules"
sudo ln -s $HOME/grand-prix/.xubuntu/opp.rules /etc/udev/rules.d/opp.rules
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=tty

# ModemManager probes new USB serial ports at boot and can confuse the
# OPP/Arduino boards. A pinball machine has no modem, so turn it off.
sudo systemctl disable --now ModemManager 2>/dev/null || true
sudo systemctl mask ModemManager 2>/dev/null || true

# Install systemd service for auto-restart
[ -f "/etc/systemd/system/grand-prix.service" ] && sudo rm "/etc/systemd/system/grand-prix.service"
sudo ln -s $HOME/grand-prix/.xubuntu/grand-prix.service /etc/systemd/system/grand-prix.service
sudo systemctl daemon-reload
echo "grand-prix ALL=(ALL) NOPASSWD: /bin/systemctl restart grand-prix, /bin/systemctl stop grand-prix, /bin/systemctl start grand-prix" | sudo tee /etc/sudoers.d/grand-prix
