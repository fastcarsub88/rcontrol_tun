#!/bin/bash
if [ ! $1 ]; then
    echo "Specify (8_relay) or (megaioind)"
    exit
fi
sudo apt-get install build-essential python3-pip python3-dev python3-smbus nginx -y
cd /home/pi
if [[ $1 == "8_relay" ]]; then
  git clone https://github.com/SequentMicrosystems/ioplus-rpi.git
  cp /home/pi/rcontrol_tun/install/ioplus.py /home/pi/rcontrol_tun/app/definitions.py
  cd ioplus-rpi/python/ioplus/
fi
if [[ $1 == "megaioind" ]]; then
  git https://github.com/SequentMicrosystems/megaioind-rpi.git
  cp /home/pi/rcontrol_tun/install/megaioind.py /home/pi/rcontrol_tun/app/definitions.py
  cd imegaioind-rpi/python/megaioind/
fi
sudo python setup.py install
sudo pip install uwsgi
sudo pip install requests
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/pi/rcontrol_tun/install/nginx_conf /etc/nginx/sites-enabled/
sudo nginx -s reload
sudo systemctl link /home/pi/rcontrol_tun/install/rcontrol_web.service
sudo systemctl link /home/pi/rcontrol_tun/install/rcontrol_sched.service
sudo systemctl enable rcontrol_web
sudo systemctl enable rcontrol_sched
sudo raspi-config nonint do_i2c 0
sudo reboot
