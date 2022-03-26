from flask import Flask
import logging
import util_mqtt

app = Flask(__name__)
logging.basicConfig(
    filename='record.log',
    level=logging.WARN,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
mqtt_client = util_mqtt.ServiceMQTTClient()

import config
import events
import run_data
import schedule

if __name__ == '__main__':
    app.run(debug = True)
