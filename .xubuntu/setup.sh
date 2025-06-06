#!/usr/bin/env bash

sudo groupadd -r autologin
sudo gpasswd -a $USER autologin

# To autologin to the Xubuntu Desktop X Server
sudo ln -s $HOME/grand-prix/.xubuntu/lightdm.conf \
  /etc/lightdm/lightdm.conf

# To launch MPF after starting the X Server
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
sudo ln -s $HOME/grand-prix/.xubuntu/opp.rules /etc/udev/rules.d/opp.rules
