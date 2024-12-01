Xubuntu Setup
=============

This is a guide to setup a production environment in
Xubuntu (24.04 LTS as of this writing).

Machine Setup
-------------

First, [install
Xubuntu](https://mirror.us.leaseweb.net/ubuntu-cdimage/xubuntu/releases/24.04/release/xubuntu-24.04.1-desktop-amd64.iso)
and when prompted during installation, select "minimal installation".

After first boot, open a terminal and run the following commands:

```sh
sudo apt-get update
sudo apt-get install openssh-server ifconfig -y
```

### Connect with `ssh`

From another machine, connect to the `ssh` server with `ssh
HOSTNAME`. Depending on your network or devices this may not work.
If not, determine the IP address of the machine with `ifconfig` and
connect to it with `ssh IP_ADDRESS`.

### Continue Setup Remotely

Install the OS-level dependencies and optionally replace the
crappy gimped `vim-tiny` with the proper package:

```sh
sudo apt-get remove vim-tiny
sudo apt-get install vim build-essential git curl libsqlite3-dev \
  zlib1g-dev libjpeg-dev libtiff5-dev libtiff5-dev \
  libsdl2-dev libsdl2-ttf-dev libsdl2-image-dev \
  libsdl2-mixer-dev gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly libgstreamer1.0-dev \
  libxine2-ffmpeg libsmpeg-dev libswscale-dev \
  libavformat-dev libavcodec-dev libjpeg-dev libtiff5-dev \
  libx11-dev libmtdev-dev build-essential libgl1-mesa-dev \
  libgles2-mesa-dev pulseaudio lsb-release \
  libgl1-mesa-dri libavfilter-dev libavdevice-dev -y
```

The `python` provided by 24.04 is higher than the currently most
stable version of `mpf` (0.57.x as of this writing), so we install
`pyenv` and `python 3.10`:

```sh
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
pyenv install 3.10
pyenv global 3.10
pip install --upgrade pip setuptools wheel build coveralls pillow
pip install --upgrade Cython==0.29.36
pip install mpf==0.57.0
pip install mpf-mc==0.57.0
pip install mpf-monitor==0.57.0
```

### Optional: Install `foreman` for Development

To develop on the machine, installing `foreman` allows running
all the services with a single command. Note that this is not
necessary for production:

```sh
gpg --keyserver hkp://keyserver.ubuntu.com \
    --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
\curl -sSL https://get.rvm.io | bash
source $HOME/.rvm/scripts/rvm
rvm pkg install openssl
rvm install 3.2.1 -C --with-openssl-dir=/usr/share/rvm/usr
rvm use 3.2.1 --default
gem install foreman
```
