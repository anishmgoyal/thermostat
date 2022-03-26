#!/bin/bash

# TODO: Move auto-dimming code into the management service
# Although, it does look fine in the dimmed state - could just keep it like this
sudo bash -c "echo 0 > /sys/class/backlight/rpi_backlight/brightness"

# Wait for the UI to load, so that we don't open a blank chromium window
until curl http://localhost:8001/thermostat.html
do
    echo "Waiting for interface to start"
    sleep 1
done

# Wait for the API to load as well, to ensure that the UI has data to drive
# it
until curl http://localhost:8001/api/config
do
    echo "Waiting for management service to start"
    sleep 1
done

/usr/bin/chromium-browser \
    --app=http://localhost:8081/thermostat.html \
    --kiosk \
    --noerrdialogs \
    --disable-session-crashed-bubble \
    --disable-infobars \
    --check-for-update-interval=604800 \
    --disable-pinch
