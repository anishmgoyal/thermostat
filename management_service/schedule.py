from flask import abort, request, Response
from main import app, mqtt_client
from tstatcommon import constants, data, mqttconstants
import json
import os
import settings
import multiprocessing
import util_validators

_LOCK = multiprocessing.Lock()


@app.route("/schedule", methods = ["GET", "POST"])
def schedule():
    if request.method == "GET":
        with open(data.filenames.SCHEDULE_FILE, "r") as schedule:
            return Response(schedule.read(), mimetype="application/json")
    else:
        new_schedule = request.get_json()
        swap_file = data.filenames.getSwapFile(data.filenames.SCHEDULE_FILE)
        if validateSchedule(new_schedule):
            with _LOCK:
                with open(swap_file, "w") as schedule:
                    schedule.write(json.dumps(new_schedule, indent = 4))
                os.replace(swap_file, data.filenames.SCHEDULE_FILE)

            mqtt_client.publishUpdateConfig(mqttconstants.CONFIG_TYPE_SCHEDULE)
            return ''
        else:
            abort(400)

def validateSchedule(schedule) -> bool:
    if data.CFG_ENTRIES not in schedule:
        app.logger.info('entries not in schedule')
        return False
    if not isinstance(schedule[data.CFG_ENTRIES], list):
        app.logger.info('entries are not a list')
        return False

    for entry in schedule[data.CFG_ENTRIES]:
        if not validateScheduleEntry(entry):
            app.logger.info('schedule had an invalid entry')
            return False

    return True

def validateScheduleEntry(entry) -> bool:
    if data.CFG_MODE not in entry:
        app.logger.info('schedule entry is missing mode')
        return False
    mode = entry[data.CFG_MODE]
    if mode not in constants.ALL_MODES or mode == constants.MODE_OFF:
        app.logger.info('schedule entry has invalid mode {}'.format(mode))
        return False
    
    if data.CFG_DAY_OF_WEEK not in entry:
        app.logger.info('schedule entry is missing day of week')
        return False
    if not util_validators.isValidIntInRange(entry[data.CFG_DAY_OF_WEEK], 0, 6):
        app.logger.info('schedule entry has out of range day of week')
        return False

    if data.CFG_START_HOUR not in entry:
        app.logger.info('schedule entry is missing start hour')
        return False
    if not util_validators.isValidIntInRange(entry[data.CFG_START_HOUR], 0, 23):
        app.logger.info('schedule entry has invalid start hour')
        return False

    if data.CFG_START_MINUTE not in entry:
        app.logger.info('schedule entry is missing start minute')
        return False
    if not util_validators.isValidIntInRange(
            entry[data.CFG_START_MINUTE], 0, 59):
        app.logger.info('schedule entry has invalid start minute')
        return False

    if data.CFG_SETTINGS not in entry:
        app.logger.info('schedule entry is missing settings')
        return False

    # Verify that the settings are valid for this entry. If the entry is for
    # auto mode, it needs both a valid heat + cool temp. Otherwise, it only
    # needs one.
    return settings.validateSettings(
        entry[data.CFG_SETTINGS],
        require_cool = mode in [constants.MODE_COOL, constants.MODE_AUTO],
        require_heat = mode in [constants.MODE_HEAT, constants.MODE_AUTO])
