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
if [[ '4ffef8c358742a3d01eaba9b07d50679eba8a816' == $NEW_HASH ]]
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

