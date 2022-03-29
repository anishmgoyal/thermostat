import build_info
import json
import logging
import multiprocessing
import paho.mqtt.client as mqtt
import queue
import uuid
from tstatcommon import mqttconstants


class ServiceMQTTConsumer(object):
    def __init__(self):
        self.is_open = True
        self.q = queue.Queue()

        start_event = {
            mqttconstants.CFG_EVENT_TYPE: mqttconstants.EVENT_CONSUMER_INIT,
            mqttconstants.CONSUMER_INIT_VER: build_info.BUILD_VER
        }
        self.addValue(json.dumps(start_event))

    def addValue(self, value):
        self.q.put(value)

    def consume(self):
        try:
            while True:
                yield "data: {}\n\n".format(self.q.get())
                self.q.task_done()
        except GeneratorExit:
            self.is_open = False
        except:
            logging.exception("Consumer was killed, marking it closed")
            self.is_open = False


class ServiceMQTTClient(object):
    def __init__(self):
        self.client = mqtt.Client(str(uuid.uuid4()))
        self.client.connect(mqttconstants.MQTT_HOSTNAME)
        self.consumer_lock = multiprocessing.Lock()
        self.consumers: list[ServiceMQTTConsumer] = []

        # Create a separate thread that sends messages to any consumers
        self.client.on_message = self.onMessage
        self.client.subscribe(mqttconstants.MQTT_TOPIC)
        self.client.loop_start()

    def addConsumer(self, consumer: ServiceMQTTConsumer):
        with self.consumer_lock:
            self.consumers.append(consumer)

    def onMessage(self,
                  client: mqtt.Client,
                  userdata,
                  message: mqtt.MQTTMessage):
        with self.consumer_lock:
            active_consumers = []
            for consumer in self.consumers:
                if consumer.is_open:
                    consumer.addValue(message.payload.decode('utf-8'))
                    active_consumers.append(consumer)
                else:
                    logging.info('Evicting an inactive consumer')
            logging.info("%d active consumers" % len(active_consumers))
            self.consumers = active_consumers

    def publishUpdateConfig(self, config_type):
        payload = {
            mqttconstants.CFG_EVENT_TYPE: mqttconstants.EVENT_UPDATE_CONFIG,
            mqttconstants.CFG_CONFIG_TYPE: config_type
        }
        self.client.publish(mqttconstants.MQTT_TOPIC, json.dumps(payload))
