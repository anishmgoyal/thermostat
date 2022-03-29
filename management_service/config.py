import logging
from flask import abort, request, Response
from main import app, mqtt_client
from tstatcommon import constants, data, mqttconstants
import json
import os
import multiprocessing
import util_validators

_LOCK = multiprocessing.Lock()


@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "GET":
        logging.info('Fetching config file')
        with open(data.filenames.CONFIG_FILE, "r") as config:
            return Response(config.read(), mimetype="application/json")
    else:
        new_config = request.get_json()
        swap_file = data.filenames.getSwapFile(data.filenames.CONFIG_FILE)
        if validateConfig(new_config):
            with _LOCK:
                with open(swap_file, "w") as config:
                    config.write(json.dumps(new_config, indent = 4))
                os.replace(swap_file, data.filenames.CONFIG_FILE)

            mqtt_client.publishUpdateConfig(mqttconstants.CONFIG_TYPE_BASE)
            return ''
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

    if data.CFG_DISPLAY_UNITS not in config:
        return False
    if config[data.CFG_DISPLAY_UNITS] not in constants.ALL_DISPLAY_UNITS:
        return False

    return True
