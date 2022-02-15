if [ ! $1 ]; then
    echo "Specify (v1) - megaio board + relay8 or (v2) megaio board only or (v3) - home automation"
    exit
fi
cd /home/pi
if [[ $1 == "v3" ]]; then
  cp /home/pi/rcontrol_tun/install/ioplus.py /home/pi/rcontrol_tun/app/definitions.py
  cd /home/pi/ioplus-rpi/python/ioplus/
fi
if [[ $1 == "v2" ]]; then
  cp /home/pi/rcontrol_tun/install/megaioind.py /home/pi/rcontrol_tun/app/definitions.py
  cd /home/pi/imegaioind-rpi/python/megaioind/
fi
if [[ $1 == "v1" ]]; then
  cp /home/pi/rcontrol_tun/install/8_relay.py /home/pi/rcontrol_tun/app/definitions.py
  cd /home/pi/imegaioind-rpi/python/megaioind/
fi
sudo rm /etc/nginx/sites-enabled/nginx_conf
sudo ln -s /home/pi/rcontrol_tun/install/nginx_conf /etc/nginx/sites-enabled/
sudo nginx -s reload
sudo systemctl stop rcontrol_web
sudo systemctl stop rcontrol_sched
sudo systemctl disable rcontrol_web
sudo systemctl disable rcontrol_sched
sudo systemctl link /home/pi/rcontrol_tun/install/rcontrol_web.service
sudo systemctl link /home/pi/rcontrol_tun/install/rcontrol_sched.service
sudo systemctl enable rcontrol_web
sudo systemctl enable rcontrol_sched
sudo systemctl start rcontrol_web
sudo systemctl start rcontrol_sched
