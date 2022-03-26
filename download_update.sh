#!/bin/bash
## GENERATED FILE, DO NOT MODIFY

# Utility methods
function do_cleanup() {
    if [[ -d /staging/thermostat ]]
    then
        rm -rf /staging/thermostat
    fi
}

# Start with cleanup
do_cleanup

# Clone the repository
mkdir -p /staging
cd /staging
git clone https://github.com/anishmgoyal/thermostat.git
cd thermostat

# Check if update needed. If not, clean up and exit
# the script
NEW_HASH=$(git show --pretty='format:%H' HEAD | head -1)
if [[ '4ca379659a85e3d6777efa3f154255ad46c91fdc' == $NEW_HASH ]]
then
    do_cleanup
    exit 0
fi

# Install the new version of the thermostat
./install.sh
INSTALL_RESULT=$?

# Clean up and return
do_cleanup
exit $INSTALL_RESULT

