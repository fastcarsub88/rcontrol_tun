#!/bin/bash
if [ ! $1 ]; then
    echo "Specify (v1) - megaio board + relay8 or (v2) megaio board only or (v3) - home automation"
    exit
fi
sudo apt-get install build-essential python3-pip python3-dev python3-smbus nginx -y
cd /home/pi
if [[ $1 == "v3" ]]; then
  git clone https://github.com/SequentMicrosystems/ioplus-rpi.git
  cp /home/pi/rcontrol_tun/install/ioplus.py /home/pi/rcontrol_tun/app/definitions.py
  cp /home/pi/rcontrol_tun/install/custom.css /home/pi/rcontrol_tun/html/custom.css
  cd /home/pi/ioplus-rpi/python/ioplus/
fi
if [[ $1 == "v2" ]]; then
  git https://github.com/SequentMicrosystems/megaioind-rpi.git
  cp /home/pi/rcontrol_tun/install/megaioind.py /home/pi/rcontrol_tun/app/definitions.py
  cp /home/pi/rcontrol_tun/install/custom.css /home/pi/rcontrol_tun/html/custom.css
  cd /home/pi/imegaioind-rpi/python/megaioind/
fi
if [[ $1 == "v1" ]]; then
  git https://github.com/SequentMicrosystems/megaioind-rpi.git
  cp /home/pi/rcontrol_tun/install/8_relay.py /home/pi/rcontrol_tun/app/definitions.py
  cp /home/pi/rcontrol_tun/install/relay8.py /home/pi/rcontrol_tun/app/
  cp /home/pi/rcontrol_tun/install/8_relay.css /home/pi/rcontrol_tun/html/custom.css
  cd /home/pi/imegaioind-rpi/python/megaioind/
fi
sudo python setup.py install
sudo pip install uwsgi
sudo pip install requests
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/pi/rcontrol_tun/install/nginx_conf /etc/nginx/sites-enabled/
sudo nginx -s reload
cp /home/pi/rcontrol_tun/app/example_data_file.json /home/pi/rcontrol_tun/app/data_file.json
cp /home/pi/rcontrol_tun/install/custom.css /home/pi/rcontrol_tun/app/custom.css
sudo systemctl link /home/pi/rcontrol_tun/install/rcontrol_web.service
sudo systemctl link /home/pi/rcontrol_tun/install/rcontrol_sched.service
sudo systemctl enable rcontrol_web
sudo systemctl enable rcontrol_sched
sudo raspi-config nonint do_i2c 0
sudo reboot
