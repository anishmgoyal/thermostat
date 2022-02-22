import paho.mqtt.client as mqtt
import json
import uuid
from tstatcommon import mqttconstants


class ServiceMQTTClient(object):

    def __init__(self):
        self.client = mqtt.Client(str(uuid.uuid4()))
        self.client.connect(mqttconstants.MQTT_HOSTNAME)

    def publishUpdateConfig(self, config_type):
        payload = {
            mqttconstants.CFG_EVENT_TYPE: mqttconstants.EVENT_UPDATE_CONFIG,
            mqttconstants.CFG_CONFIG_TYPE: config_type
        }
        self.client.publish(mqttconstants.MQTT_TOPIC, json.dumps(payload))

