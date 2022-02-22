import data.filenames as filenames
import data.settings as settings
import json
import tstatcommon.constants

CFG_ACTIVE_MODE = 'active_mode'
CFG_BEHAVIOR = 'behavior'
CFG_FAN_ENABLED = 'fan_enabled'


class RunData(object):
    def __init__(self):
        self.file_name = filenames.RUNDATA_FILE
        self.reload()

    def getActiveMode(self) -> int:
        if CFG_ACTIVE_MODE in self.run_data:
            return self.run_data[CFG_ACTIVE_MODE]
        return tstatcommon.constants.MODE_OFF

    def getBehavior(self) -> int:
        if CFG_BEHAVIOR in self.run_data:
            return self.run_data[CFG_BEHAVIOR]
        return tstatcommon.constants.BEHAVE_SCHED

    def getFanEnabled(self) -> bool:
        if CFG_FAN_ENABLED in self.run_data:
            return self.run_data[CFG_FAN_ENABLED]
        DEFAULT_FAN_ENABLED = False
        return DEFAULT_FAN_ENABLED

    def getSettings(self):
        if settings.CFG_SETTINGS not in self.run_data:
            return settings.Settings({})
        else:
            return settings.Settings(self.run_data[settings.CFG_SETTINGS])

    def reload(self):
        with open(self.file_name, 'r') as run_data:
            self.run_data = json.load(run_data)
