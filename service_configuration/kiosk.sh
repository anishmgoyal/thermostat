#!/bin/bash

# TODO: Move auto-dimming code into the management service
# Although, it does look fine in the dimmed state - could just keep it like this
sudo bash -c "echo 0 > /sys/class/backlight/rpi_backlight/brightness"

/usr/bin/chromium-browser \
    --kiosk http://localhost:8001/thermostat.html \
    --noerrdialogs \
    --disable-session-crashed-bubble \
    --disable-infobars \
    --check-for-update-interval=604800 \
    --disable-pinch
