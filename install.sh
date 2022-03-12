#!/bin/bash
CURRENT_DIR=$(dirname $0)
BASE_DIR=/var/lib/thermostat

function reinit_dir() {
    local dirname=$1
    if [[ -f $dirname ]]
    then
        rm -rf $dirname
    fi
    mkdir -p $dirname
}

# Generate any git hash related files
./generate_git_files.sh

# Copy update code
UPDATE_DIR=$BASE_DIR/updates
reinit_dir $UPDATE_DIR
cp download_update.sh $UPDATE_DIR/.

# Install requirements
python3 -m pip install -r requirements.txt

# Copy the controller code
CONTROL_DIR=$BASE_DIR/control
reinit_dir $CONTROL_DIR
cp -r thermostat_controller/* $CONTROL_DIR/.
cp -r tstatcommon $CONTROL_DIR/.

# Copy default configuration. For now, overwrite whatever is there
DATA_DIR=$BASE_DIR/data
reinit_dir $DATA_DIR
cp -r default_config/* $DATA_DIR/.

# Copy the management service
MANAGEMENT_SERVICE_DIR=$BASE_DIR/management
reinit_dir $MANAGEMENT_SERVICE_DIR
cp -r management_service/* $MANAGEMENT_SERVICE_DIR/.
cp -r tstatcommon $MANAGEMENT_SERVICE_DIR/.
