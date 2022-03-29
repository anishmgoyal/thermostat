#!/bin/bash

echo "Waiting for interface to initialize"

# Wait for the UI to load, so that we don't open a blank chromium window
until curl -f -L http://localhost:8001/thermostat.html > /dev/null 2>&1
do
    sleep 1
done

echo "Waiting for service to initialize"

# Wait for the API to load as well, to ensure that the UI has data to drive
# it
until curl -f -L http://localhost:8001/api/config > /dev/null 2>&1
do
    sleep 1
done

[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor
