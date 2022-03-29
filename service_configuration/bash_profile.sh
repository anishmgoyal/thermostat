#!/bin/bash

# Wait for the UI to load, so that we don't open a blank chromium window
until curl -f -L http://localhost:8001/thermostat.html
do
    echo "Waiting for interface to start"
    sleep 1
done

# Wait for the API to load as well, to ensure that the UI has data to drive
# it
until curl -f -L http://localhost:8001/api/config
do
    echo "Waiting for management service to start"
    sleep 1
done

[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor
