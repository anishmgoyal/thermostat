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
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y nginx mosquitto
python3 -m pip install -r requirements.txt

# Setup nginx
cp service_configuration/nginx.conf /etc/nginx/.
mkdir -p /etc/nginx/servers/
cp service_configuration/default_nginx_site.conf /etc/nginx/servers/.
sudo /etc/init.d/nginx -s restart

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

# Copy the updater service; do not bounce, since we rely on this service for
# running updates start to finish. This service can be bounced manually if
# updated.
VERSIONS_SERVICE_DIR=$BASE_DIR/versions
reinit_dir $VERSIONS_SERVICE_DIR
cp -r update_service/* $VERSIONS_SERVICE_DIR

# Install services
cp service_configuration/thermostat_controller.service /etc/systemd/system/.
cp service_configuration/thermostat_management.service /etc/systemd/system/.
cp service_configuration/thermostat_versions.service /etc/systemd/system/.

sudo systemctl enable mosquitto.service --now
sudo systemctl enable thermostat_versions.service --now
SERVICES=(thermostat_controller thermostat_management)
for service in ${SERVICES[@]}
do
    sudo systemctl enable $service --now
    sudo systemctl restart $service
done
