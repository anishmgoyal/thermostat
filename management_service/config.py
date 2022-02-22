from flask import abort, request
from main import app, mqtt_client
from tstatcommon import data, mqttconstants
import os
import util_validators


@app.request("/config", methods=["GET", "SET"])
def config():
    if request.method == "GET":
        with open(data.filenames.CONFIG_FILE, "r") as config:
            return config.read()
    else:
        new_config = request.get_json()
        swap_file = data.filenames.getSwapFile(data.filenames.CONFIG_FILE)
        if validateConfig(new_config):
            with open(swap_file, "w") as config:
                config.write(new_config)
            os.replace(swap_file, data.filenames.CONFIG_FILE)

            mqtt_client.publishUpdateConfig(mqttconstants.CONFIG_TYPE_BASE)
        else:
            abort(400)


def validateConfig(config):
    if data.CFG_THERMOSTAT_EPSILON not in config:
        return False
    if not util_validators.isValidNumberInRange(
            config[data.CFG_THERMOSTAT_EPSILON],
            0.2,
            2.0):
        return False

    return True
