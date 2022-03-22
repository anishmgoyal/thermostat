import tstatcommon.data.filenames as filenames
import tstatcommon.data.settings as settings
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
        """ Get the settings for the current active mode """
        active_mode = self.getActiveMode()
        if active_mode == tstatcommon.constants.MODE_OFF:
            return settings.Settings({}) # special case. Settings are null for
                                         # mode "off"
        if settings.CFG_SETTINGS not in self.run_data:
            return settings.Settings({})
        elif active_mode not in range(
                len(self.run_data[settings.CFG_SETTINGS])):
            return settings.Settings({})
        else:
            return settings.Settings(
                self.run_data[settings.CFG_SETTINGS][active_mode])

    def reload(self):
        with open(self.file_name, 'r') as run_data:
            self.run_data = json.load(run_data)
