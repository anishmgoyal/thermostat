import digitalio
import json
import RPi.GPIO as gpio
from flask import Response
from main import app
from tstatcommon import circuit

# Convert truthy/falsy pin values to booleans
def pin_value(pin: digitalio.Pin):
    if gpio.input(pin.id):
        return True
    return False

@app.route("/current_state", methods=["GET"])
def current_state():
    if pin_value(circuit.POWER_PIN) == circuit.POWER_FAN:
        mode = 'off'
    elif pin_value(circuit.CONTROL_PIN) == circuit.CONTROL_COOL:
        mode = 'cool'
    else:
        mode = 'heat'

    fan_enabled = pin_value(circuit.FAN_PIN) == circuit.FAN_ON

    payload = {
        "mode": mode,
        "fan": "on" if fan_enabled else "auto"
    }
    return Response(json.dumps(payload), mimetype="text/json")
