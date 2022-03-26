#!/bin/bash
CURRENT_DIR=$(dirname $0)
BASE_DIR=/var/lib/thermostat
STAGING_DIR=/staging
IAM=$(whoami)

if [[ ! -d $BASE_DIR ]]
then
    sudo mkdir $BASE_DIR
    sudo chown -R $IAM:$IAM $BASE_DIR
fi

if [[ ! -d $STAGING_DIR ]]
then
    sudo mkdir $STAGING_DIR
    sudo chown -R $IAM:$IAM $STAGING_DIR
fi

function reinit_dir() {
    local dirname=$1
    if [[ -d $dirname ]]
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
sudo apt-get install -y nginx mosquitto python3 iptables
python3 -m pip install -r requirements.txt

# Setup nginx
sudo cp service_configuration/nginx.conf /etc/nginx/.
mkdir -p /etc/nginx/servers/
sudo cp service_configuration/default_nginx_site.conf /etc/nginx/servers/.
sudo systemctl restart nginx

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

# Copy the user interface
USER_INTERFACE_DIR=$BASE_DIR/interface
reinit_dir $USER_INTERFACE_DIR
cp -r user_interface/* $USER_INTERFACE_DIR/.

# Copy the updater service; do not bounce, since we rely on this service for
# running updates start to finish. This service can be bounced manually if
# updated.
# We also want to make sure that we don't delete the socket file, if it exists
VERSIONS_SERVICE_DIR=$BASE_DIR/versions
mkdir -p $VERSIONS_SERVICE_DIR
find $VERSIONS_SERVICE_DIR -not -name 'service.sock' -delete
cp -r update_service/* $VERSIONS_SERVICE_DIR

# Install services
sudo cp service_configuration/thermostat_controller.service /etc/systemd/system/.
sudo cp service_configuration/thermostat_management.service /etc/systemd/system/.
sudo cp service_configuration/thermostat_versions.service /etc/systemd/system/.

sudo systemctl enable mosquitto.service --now
sudo systemctl enable thermostat_versions.service --now
SERVICES=(thermostat_controller thermostat_management)
for service in ${SERVICES[@]}
do
    sudo systemctl enable $service --now
    sudo systemctl restart $service
done

# Configure iptables
function add_iptable_rule()
    local rule=$1
    sudo iptables -C $rule || sudo iptables -A $rule
fi

add_iptable_rule "INPUT -p tcp -s 192.168.1.0/24 -j ACCEPT"
add_iptable_rule "INPUT -p tcp -s 192.168.4.0/24 -j ACCEPT"
add_iptable_rule "INPUT -p tcp -s 127.0.0.0/8 -j ACCEPT"
add_iptable_rule "INPUT -p tcp -j REJECT"
