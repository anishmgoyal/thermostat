#!/bin/bash

python3 -m pip install -r requirements.txt
mkdir -p /var/lib/thermostat/control
cp -r src /var/lib/thermostat/control

mkdir /var/lib/thermostat/control/data
cp -r config/* /var/lib/thermostat/control/data/.
cp -r ../tstatcommon /var/lib/thermostat/control/src/.