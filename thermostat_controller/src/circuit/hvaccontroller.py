import board
import data
import digitalio
import logging
import time
import RPi.GPIO as gpio

HEAT_PIN = board.D21
COOL_PIN = board.D20
FAN_PIN = board.D26

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


def _loadPin(pin: digitalio.Pin) -> digitalio.DigitalInOut:
    # Before initializing digitalio, check
    # what this circuit's current state is
    gpio.setup(pin.id, gpio.OUT)
    current_value = gpio.input(pin.id)

    gpio_pin = digitalio.DigitalInOut(pin)
    gpio_pin.switch_to_output(value=current_value)
    return gpio_pin


class HVACController(object):
    def __init__(self, recent_activity: data.RecentActivity):
        self.recent_activity = recent_activity
        self.control_pin = _loadPin(CONTROL_PIN)
        self.power_pin = _loadPin(POWER_PIN)
        self.fan_pin = _loadPin(FAN_PIN)

    @property
    def is_heat_on(self) -> bool:
        return self.control_pin.value == CONTROL_HEAT and \
            self.power_pin.value == POWER_TEMP

    @property
    def is_cool_on(self) -> bool:
        return self.control_pin.value == CONTROL_COOL and \
            self.power_pin.value == POWER_TEMP

    @property
    def is_fan_on(self) -> bool:
        # This property works differently than the other
        # properties. We care more about the
        return self.fan_pin.value

    def enableHeat(self):
        # Safety measure - do not switch directly from
        # heat to cool
        if self.is_cool_on:
            logging.warning("Cannot enable heat with cooling on")
            self.shutDown()
            return

        # Safety measure - make sure we are eligible for
        # a heat toggle now
        if self.recent_activity.canToggle():
            self.recent_activity.setLastHeatEnableTime(time.time())
            self.control_pin.value = CONTROL_HEAT
            self.power_pin.value = POWER_TEMP
        else:
            logging.warning("Cannot enable heat right now")

    def enableCool(self):
        # Safety measure - do not switch directly from
        # cool to heat
        if self.is_heat_on:
            logging.warning("Cannot enable cooling with heat on")
            self.shutDown()
            return

        # Safety measure - make sure we are eligible for
        # a cooling toggle now
        if self.recent_activity.canToggle():
            self.recent_activity.setLastCoolEnableTime(time.time())
            self.control_pin.value = CONTROL_COOL
            self.power_pin.value = POWER_TEMP
        else:
            logging.warning("Cannot enable cooling right now")

    def shutDown(self):
        # Safety measure - do not disable cooling unless it's been
        # on for some amount of time
        if self.is_cool_on:
            if self.recent_activity.canToggle():
                self.recent_activity.setLastCoolDisableTime(time.time())
                self.power_pin.value = POWER_FAN
            else:
                logging.warning("Cannot disable cooling right now")
        # Safety measure - do not disable heating unless it's been
        # on for some amount of time
        elif self.is_heat_on:
            if self.recent_activity.canToggle():
                self.recent_activity.setLastHeatDisableTime(time.time())
                self.power_pin.value = POWER_FAN
            else:
                logging.warning("Cannot disable cooling right now")

    def enableFan(self):
        self.fan_pin.value = FAN_ON

    def disableFan(self):
        self.fan_pin.value = FAN_AUTO
