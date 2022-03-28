import board

CONTROL_PIN = board.D21  # Switches between hot/cold
POWER_PIN = board.D20   # Switches power from temp / fan
FAN_PIN = board.D26     # Enables the fan, if the fan circuit is on

# Values fo the power pin, specifying what circuit should be
# enabled
POWER_TEMP = True
POWER_FAN = False

# Values for the control pin, specifying if the system should
# heat or cool
CONTROL_HEAT = False
CONTROL_COOL = True

# Values for the fan pin, specifying if the fan should be
# forced to ON, or AUTO
FAN_AUTO = False
FAN_ON = True
