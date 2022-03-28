import controlmqtt
import digitalio
import logging
import socket
import time
import tstatcommon.circuit as circuit
import tstatcommon.data as data
import tstatcommon.mqttconstants as mqttconstants
import RPi.GPIO as gpio

def _loadPin(pin: digitalio.Pin) -> digitalio.DigitalInOut:
    # Before initializing digitalio, check
    # what this circuit's current state is
    gpio.setup(pin.id, gpio.OUT)
    current_value = gpio.input(pin.id)

    gpio_pin = digitalio.DigitalInOut(pin)
    gpio_pin.switch_to_output(value=current_value)
    return gpio_pin


class HVACController(object):
    def __init__(self,
                 mqtt_client: controlmqtt.ControlMQTTClient,
                 recent_activity: data.RecentActivity):
        self.mqtt_client = mqtt_client
        self.recent_activity = recent_activity
        self.control_pin = _loadPin(circuit.CONTROL_PIN)
        self.power_pin = _loadPin(circuit.POWER_PIN)
        self.fan_pin = _loadPin(circuit.FAN_PIN)

    @property
    def is_heat_on(self) -> bool:
        return self.control_pin.value == circuit.CONTROL_HEAT and \
            self.power_pin.value == circuit.POWER_TEMP

    @property
    def is_cool_on(self) -> bool:
        return self.control_pin.value == circuit.CONTROL_COOL and \
            self.power_pin.value == circuit.POWER_TEMP

    @property
    def is_fan_on(self) -> bool:
        # This property works differently than the other
        # properties. We care more about the
        return self.fan_pin.value

    def sendStateChangeEvent(self):
        if self.is_heat_on:
            mode = mqttconstants.STATE_CHANGE_MODE_HEATING
        elif self.is_cool_on:
            mode = mqttconstants.STATE_CHANGE_MODE_COOLING
        else:
            mode = mqttconstants.STATE_CHANGE_MODE_OFF

        if self.is_fan_on:
            fan = mqttconstants.STATE_CHANGE_FAN_ON
        else:
            fan = mqttconstants.STATE_CHANGE_FAN_AUTO

        base_ev = {
            mqttconstants.CFG_EVENT_TYPE: mqttconstants.EVENT_STATE_CHANGE,
            mqttconstants.CFG_STATE_CHANGE_HOSTNAME: socket.gethostname(),
            mqttconstants.CFG_STATE_CHANGE_MODE: mode,
            mqttconstants.CFG_STATE_CHANGE_FAN: fan
        }
        self.mqtt_client.sendEvent(base_ev)

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
            self.control_pin.value = circuit.CONTROL_HEAT
            self.power_pin.value = circuit.POWER_TEMP
            self.sendStateChangeEvent()
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
            self.control_pin.value = circuit.CONTROL_COOL
            self.power_pin.value = circuit.POWER_TEMP
            self.sendStateChangeEvent()
        else:
            logging.warning("Cannot enable cooling right now")

    def shutDown(self):
        # Safety measure - do not disable cooling unless it's been
        # on for some amount of time
        if self.is_cool_on:
            if self.recent_activity.canToggle():
                self.recent_activity.setLastCoolDisableTime(time.time())
                self.power_pin.value = circuit.POWER_FAN
                self.sendStateChangeEvent()
            else:
                logging.warning("Cannot disable cooling right now")
        # Safety measure - do not disable heating unless it's been
        # on for some amount of time
        elif self.is_heat_on:
            if self.recent_activity.canToggle():
                self.recent_activity.setLastHeatDisableTime(time.time())
                self.power_pin.value = circuit.POWER_FAN
                self.sendStateChangeEvent()
            else:
                logging.warning("Cannot disable cooling right now")

    def enableFan(self):
        self.fan_pin.value = circuit.FAN_ON
        self.sendStateChangeEvent()

    def disableFan(self):
        self.fan_pin.value = circuit.FAN_AUTO
        self.sendStateChangeEvent()
