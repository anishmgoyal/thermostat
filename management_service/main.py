from flask import Flask
import util_mqtt

app = Flask(__name__)
mqtt_client = util_mqtt.ServiceMQTTClient()

import config
import events
import run_data
import schedule

if __name__ == '__main__':
    app.run(debug = True)
