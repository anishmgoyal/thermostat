# Therm14 Processes

## Host

The primary thermostat will have the hostname `therm14`
Any satellite thermostats should have different hostnames,
but we won't be building support for that right now,
especially since we aren't adding a setup module / i18n /
any of those other goodies.

This approach will ensure a local broker for services,
allowing for future enhancements, while not committing to
them.

## MQTT

Host `therm14` will have a mosquitto MQTT broker installed,
with some password set by us, and hardcoded into the system.
We're going to set the broker to only accept connections from
the local subnet. We'll bind to wlan0, and define firewall
rules on that interface for this restriction.

If someone wants to change the password, they are welcome to,
but this will have to be done manually.

## Thermostat Control Module

This module will listen to the sensor, as well as MQTT when
possible, to keep track of important status changes.

Milestone 1 will only support mode change events, which will
be sent by the management service (described in the next
section). The thermostat control module will then keep track
of the current schedule state, current temperature, and recent
state changes, in order to decide what circuits to enable or
disable. This module will tick once every 2 seconds to decide
if a change should be made.

Every minute, the module will check the schedule to see if
the schedule has been updated, and apply new settings. We can
have a ticker that keeps track of how many iterations we've
gone through.

## Thermostat Management API

The management API will support the following operations:
- Get + set current setting as hold / schedule
    - If setting hold, should take a ThermostatSetting object
- Patch thermostat schedule (maybe we should do a full write?)

## External Temperature Sensor

Reportings of temperature will be done twice a minute, and
will send the average reading calculated during that period.
The temperature readings will be done every two seconds, for
a max of 15 readings per reporting.

