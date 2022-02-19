#!/bin/bash

python3 -m pip install -r requirements.txt
rm -rf /var/lib/thermostat
mkdir -p /var/lib/thermostat/control/data
cp -r src /var/lib/thermostat/control

cp -r config/* /var/lib/thermostat/control/data/.
cp -r ../tstatcommon /var/lib/thermostat/control/src/.