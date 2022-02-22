#!/bin/bash

BASE_DIR=/var/lib/thermostat

# Copy requirements
python3 -m pip install -r requirements.txt

# Copy the controller code
CONTROL_DIR=$BASE_DIR/control
rm -rf $CONTROL_DIR
mkdir -p $CONTROL_DIR
cp -r thermostat_controller/* $CONTROL_DIR/.
cp -r tstatcommon $CONTROL_DIR/.

# Copy default configuration. For now, overwrite whatever is there
DATA_DIR=$BASE_DIR/data
rm -rf $DATA_DIR
mkdir -p $DATA_DIR
cp -r default_config/* $DATA_DIR/.
