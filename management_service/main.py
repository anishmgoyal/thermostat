from flask import Flask
import util_mqtt

app = Flask(__name__)
mqtt_client = util_mqtt.ServiceMQTTClient()

# TODO: Consider adding @app.before_request to check a request signature
# This service is intended to run behind a firewall, but it is good practice
# to use signed requests
