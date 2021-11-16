#!/bin/bash

sudo apt-get install build-essential python3-pip python3-dev python3-smbus nginx -y
cd /home/pi
git clone https://github.com/SequentMicrosystems/megaioind-rpi.git
cd megaioind-rpi/python/megaioind/
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
