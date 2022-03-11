from flask import Response
import util_mqtt
from main import app, mqtt_client

@app.route("/events")
def events():
    consumer = util_mqtt.ServiceMQTTConsumer()
    mqtt_client.addConsumer(consumer)
    Response(consumer.consume(), mimetype="text/event-stream")
