import digitalio
import json
from flask import Response
from main import app
from tstatcommon import circuit

CONTROL_PIN = digitalio.DigitalInOut(circuit.CONTROL_PIN)
CONTROL_PIN.switch_to_input()
POWER_PIN = digitalio.DigitalInOut(circuit.POWER_PIN)
POWER_PIN.switch_to_input()
FAN_PIN = digitalio.DigitalInOut(circuit.FAN_PIN)
FAN_PIN.switch_to_input()

@app.route("/current_state", methods=["GET"])
def current_state():
    if POWER_PIN.value == circuit.POWER_FAN:
        mode = 'off'
    elif CONTROL_PIN.value == circuit.CONTROL_COOL:
        mode = 'cool'
    else:
        mode = 'heat'

    fan_enabled = FAN_PIN.value == circuit.FAN_ON

    payload = {
        "mode": mode,
        "fan": "on" if fan_enabled else "auto"
    }
    return Response(json.dumps(payload), mimetype="text/json")
