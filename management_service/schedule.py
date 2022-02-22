from flask import abort, request
from main import app, mqtt_client
from tstatcommon import constants, data, mqttconstants
import json
import os
import settings
import util_validators

@app.route("/schedule", methods = ["GET", "POST"])
def getSchedule():
    if request.method == "GET":
        with open(data.filenames.SCHEDULE_FILE, "r") as schedule:
            return schedule.read()
    else:
        new_schedule = request.get_json()
        swap_file = data.filenames.getSwapFile(data.filenames.SCHEDULE_FILE)
        if validateScheduleEntry(new_schedule):
            with open(swap_file, "w") as schedule:
                schedule.write(json.dump(new_schedule))
            os.replace(swap_file, data.filenames.SCHEDULE_FILE)

            mqtt_client.publishUpdateConfig(mqttconstants.CONFIG_TYPE_SCHEDULE)
        else:
            abort(400)

def validateSchedule(schedule) -> bool:
    if data.CFG_ENTRIES not in schedule:
        return False
    if not isinstance(schedule[data.CFG_ENTRIES], list):
        return False

    for entry in schedule[data.CFG_ENTRIES]:
        if not validateScheduleEntry(entry):
            return False

    return True

def validateScheduleEntry(entry) -> bool:
    if data.CFG_MODE not in entry:
        return False
    mode = entry[data.CFG_MODE]
    if mode not in constants.ALL_MODES or mode == constants.MODE_OFF:
        return False
    
    if data.CFG_DAY_OF_WEEK not in entry:
        return False
    if not util_validators.isValidIntInRange(entry[data.CFG_DAY_OF_WEEK], 0, 6):
        return False

    if data.CFG_START_HOUR not in entry:
        return False
    if not util_validators.isValidIntInRange(entry[data.CFG_START_HOUR], 0, 23):
        return False

    if data.CFG_START_MINUTE not in entry:
        return False
    if not util_validators.isValidIntInRange(
            entry[data.CFG_START_MINUTE], 0, 59):
        return False

    if data.CFG_SETTINGS not in entry:
        return False

    # Verify that the settings are valid for this entry. If the entry is for
    # auto mode, it needs both a valid heat + cool temp. Otherwise, it only
    # needs one.
    return settings.validateSettings(
        entry[data.CFG_SETTINGS],
        require_cool = mode in [constants.MODE_COOL, constants.MODE_AUTO],
        require_heat = mode in [constants.MODE_HEAT, constants.MODE_AUTO])
