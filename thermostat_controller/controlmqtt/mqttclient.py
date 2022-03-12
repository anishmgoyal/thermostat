import json
import logging
import paho.mqtt.client as mqtt
from tstatcommon import data, mqttconstants
from typing import Any, Dict

# This is why this thermostat is limited to one-per-network. In order to support
# multiple per network, we'd have to be able to give satellite thermostats their
# own names (probably by configuring the thermostat to understand that it is
# not the hub thermostat, and using randoms). Right now, we don't have an
# initial configuration step, so we'll avoid attempting this.
THERMOSTAT_CLIENT_ID = 'amg_thermostat_hub_control'


class ControlMQTTClient(object):
    """
    Subscribes to the thermostat event bus. This is shoddily designed to use a
    single topic for data from ALL sensors, as well as all types of events. This
    is done for simplicity, due to the low volume of data. In high-volume
    use-cases, we'd want to segregate this data, and pay attention to the volume
    of each type of event we can get
    """
    def __init__(self,
                 config: data.Config,
                 run_data: data.RunData,
                 schedule: data.Schedule):
        self.config = config
        self.run_data = run_data
        self.schedule = schedule

        def onMessage(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
            self.takeEvent(json.loads(message.payload.decode('utf-8')))

        self.client = mqtt.Client(THERMOSTAT_CLIENT_ID)
        self.client.on_message = onMessage

    def __enter__(self):
        self.client.connect(mqttconstants.MQTT_HOSTNAME)
        self.client.loop_start()
        self.client.subscribe(mqttconstants.MQTT_TOPIC)
        return self

    def __exit__(self):
        self.client.unsubscribe(mqttconstants.MQTT_TOPIC)
        self.client.loop_stop()
        self.client.disconnect()

    def sendEvent(self, event: Dict[str, Any]):
        """ Sends an MQTT event to the common topic """
        if mqttconstants.CFG_EVENT_TYPE not in event:
            logging.error("Ignoring event with no type: {}".format(event))
            return
        self.client.publish(mqttconstants.MQTT_TOPIC, json.dumps(event))

    def takeEvent(self, event: Dict[str, Any]):
        """ Parses and acts on an MQTT event """
        if mqttconstants.CFG_EVENT_TYPE not in event:
            logging.error("Ignoring event with no type: {}".format(event))
            return
        event_type = event[mqttconstants.CFG_EVENT_TYPE]
        if event_type == mqttconstants.EVENT_UPDATE_CONFIG:
            self.reloadConfigurationFile(event)
        elif event_type == mqttconstants.EVENT_SENSOR_READING:
            self.recordSensorReading(event)

    def reloadConfigurationFile(self, event: Dict[str, Any]):
        if mqttconstants.CFG_CONFIG_TYPE not in event:
            logging.error("Ignoring config reload event with no type: {}"
                          .format(event))
            return
        config_type = event[mqttconstants.CFG_CONFIG_TYPE]
        if config_type == mqttconstants.CONFIG_TYPE_BASE:
            self.config.reload()
        elif config_type == mqttconstants.CONFIG_TYPE_RUNDATA:
            self.run_data.reload()
        elif config_type == mqttconstants.CONFIG_TYPE_SCHEDULE:
            self.schedule.reload()
        else:
            logging.error(
                "Not reloading unknown configuration %s" % config_type)

    def recordSensorReading(self, event: Dict[str, Any]):
        """
        TODO: Take sensor readings from external thermometers into account,
        and use current thermostat settings to determine which value to use
        """
        pass
