from flask import Flask
import util_mqtt

app = Flask(__name__)
mqtt_client = util_mqtt.ServiceMQTTClient()

# TODO: Add @app.before_request to check a request signature
# This service is intended to run behind a firewall, but checking a
# signed request is never a bad idea. It does complicate setup of this
# device, somewhat, but is good practice.
