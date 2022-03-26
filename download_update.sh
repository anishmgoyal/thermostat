## GENERATED FILE, DO NOT MODIFY

# Utility methods
function do_cleanup() {
    if [[ -f /staging/thermostat ]]
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
if [[ '10bfeac2d120b1b6e4fe7182fe5826005128f019' == $NEW_HASH ]]
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

