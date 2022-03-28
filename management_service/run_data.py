from flask import abort, request, Response
from main import app, mqtt_client
from tstatcommon import constants, data, mqttconstants
import json
import os
import settings
import tstatcommon


@app.route("/run_data", methods=["GET", "POST"])
def runData():
    if request.method == "GET":
        with open(data.filenames.RUNDATA_FILE, "r") as run_data:
            return Response(run_data.read(), mimetype="application/json")
    else:
        new_run_data = request.get_json()
        swap_file = data.filenames.getSwapFile(data.filenames.RUNDATA_FILE)
        if validateRunData(new_run_data):
            # write to the swap file to prevent data corruption mid-write
            with open(swap_file, "w") as run_data:
                run_data.write(json.dumps(new_run_data, indent = 4))
            # now that we've written the file fully, update the inodes on the
            # file system
            os.replace(swap_file, data.filenames.RUNDATA_FILE)

            mqtt_client.publishUpdateConfig(mqttconstants.CONFIG_TYPE_RUNDATA)
            return ''
        else:
            abort(400) # Invalid request


def validateRunData(run_data) -> bool:
    if data.CFG_ACTIVE_MODE not in run_data:
        return False
    if run_data[data.CFG_ACTIVE_MODE] not in tstatcommon.constants.ALL_MODES:
        return False

    if data.CFG_BEHAVIOR not in run_data:
        return False
    if run_data[data.CFG_BEHAVIOR] not in tstatcommon.constants.ALL_BEHAVIORS:
        return False

    if data.CFG_FAN_ENABLED not in run_data:
        return False
    if not isinstance(run_data[data.CFG_FAN_ENABLED], bool):
        return False

    if data.CFG_SETTINGS not in run_data:
        return False
    
    if len(constants.ALL_MODES) != 4:
        raise RuntimeError(
            'Implemented to support 4 modes, got a different number')

    if len(run_data[data.CFG_SETTINGS]) != len(constants.ALL_MODES):
        return False

    # validate settings for each supported mode

    if run_data[data.CFG_SETTINGS][constants.MODE_OFF] is not None:
        return False

    if not settings.validateSettings(
            run_data[data.CFG_SETTINGS][constants.MODE_COOL],
            require_cool=True):
        return False

    if not settings.validateSettings(
            run_data[data.CFG_SETTINGS][constants.MODE_HEAT],
            require_heat=True):
        return False

    if not settings.validateSettings(
            run_data[data.CFG_SETTINGS][constants.MODE_AUTO],
            require_cool=True,
            require_heat=True):
        return False
    return True
