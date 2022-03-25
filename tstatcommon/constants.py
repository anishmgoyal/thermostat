LOCAL_DEV_MODE = False # enable for local dev mode

# Defines the supported behaviors for the thermostat,
# hold + schedule.
(BEHAVE_HOLD, BEHAVE_SCHED) = range(2)

# Set of all supported behaviors
ALL_BEHAVIORS = set([BEHAVE_HOLD, BEHAVE_SCHED])

# Constants for whether or not a circuit is on.
(CIRCUIT_ON, CIRCUIT_OFF) = range(2)

# Set of all supported circuit states
ALL_CIRCUIT_STATES = set([CIRCUIT_ON, CIRCUIT_OFF])

# Constants for different operational modes of the
# thermostat. Most are self-explanatory. MODE_AUTO
# means that the thermostat will switch between heating
# and cooling, depending on the thresholds for both.
(MODE_OFF, MODE_COOL, MODE_HEAT, MODE_AUTO) = range(4)

# Set of all supported modes
ALL_MODES = set([MODE_OFF, MODE_COOL, MODE_HEAT, MODE_AUTO])

# Constants for different display units
DISPLAY_FAHREN = 'f'
DISPLAY_CELSIUS = 'c'

# Set of all supported display units
ALL_DISPLAY_UNITS = set([DISPLAY_FAHREN, DISPLAY_CELSIUS])
