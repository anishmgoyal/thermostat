# Defines the supported behaviors for the thermostat,
# hold + schedule.
(BEHAVE_HOLD, BEHAVE_SCHED) = range(2)

# Constants for whether or not a circuit is on.
(CIRCUIT_ON, CIRCUIT_OFF) = range(2)

# Constants for different operational modes of the
# thermostat. Most are self-explanatory. MODE_AUTO
# means that the thermostat will switch between heating
# and cooling, depending on the thresholds for both.
(MODE_OFF, MODE_COOL, MODE_HEAT, MODE_AUTO) = range(4)
