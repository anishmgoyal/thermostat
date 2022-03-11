## GENERATED FILE, DO NOT MODIFY

# Utility methods
function do_cleanup() {
    if [[ -f /staging/thermostat ]]
    then
        rm -rf /staging/thermostat
    fi
}

# Clone the repository
mkdir -p /staging
cd /staging
git clone git@github.com:anishmgoyal/thermostat.git
cd thermostat

# Check if update needed. If not, clean up and exit
# the script
NEW_HASH=$(git show --pretty='format:%H' head | head -1)
if [[ -eq 'de5e0cf84b61af54fec98df8c299bf4199b3494f' $NEW_HASH ]]
then
    do_cleanup
    exit 0
fi

# TODO: Add logic for stopping the current services
# systemctl stop therm-controller
# systemctl stop therm-management-service

# Install the new version of the thermostat
./install.sh
INSTALL_RESULT=$?

# Clean up and return
do_cleanup
exit $INSTALL_RESULT

