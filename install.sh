#!/bin/bash

mkdir /opt/rgbcontrol/
cp -R . /opt/rgbcontrol/
chmod +x /opt/rgbcontrol/web.py
cp /opt/rgbcontrol/rgbcontrol.service /lib/systemd/system/rgbcontrol.service
systemctl enable rgbcontrol.service
systemctl start rgbcontrol.service
