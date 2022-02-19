import data.filenames as filenames
import json
import time

CFG_LAST_HEAT_DISABLE_TIME = 'last_heat_disable_time'
CFG_LAST_HEAT_ENABLE_TIME = 'last_heat_enable_time'
CFG_LAST_COOL_DISABLE_TIME = 'last_cool_disable_time'
CFG_LAST_COOL_ENABLE_TIME = 'last_cool_enable_time'

CHANGE_THRESHOLD_TIME_SECONDS = 300


class RecentActivity(object):
    def __init__(self):
        self.file_name = filenames.RECENT_ACTIVITY_FILE
        with open(self.file_name, 'r') as recent_activity:
            self.recent_activity = json.load(recent_activity)

    def canToggleHeat(self) -> bool:
        """ Make sure that cooling has been off for at least 5
            mins, and that we haven't recently cycled heating """
        now = time.time()
        heat_disable = self.getLastHeatDisableTime()
        heat_enable = self.getLastHeatEnableTime()
        cool_disable = self.getLastCoolDisableTime()
        cool_enable = self.getLastCoolEnableTime()

        return (
            cool_enable < cool_disable and
            now - cool_disable <= CHANGE_THRESHOLD_TIME_SECONDS and
            now - max(heat_enable, heat_disable) <= CHANGE_THRESHOLD_TIME_SECONDS)

    def canToggleCool(self) -> bool:
        """ Make sure that heating has been off for at least 5
            mins, and that we haven't recently cycled cooling """
        now = time.time()
        heat_disable = self.getLastHeatDisableTime()
        heat_enable = self.getLastHeatEnableTime()
        cool_disable = self.getLastCoolDisableTime()
        cool_enable = self.getLastCoolEnableTime()

        return (
            heat_enable < heat_disable and
            now - heat_disable <= CHANGE_THRESHOLD_TIME_SECONDS and
            now - max(cool_enable, cool_disable) <= CHANGE_THRESHOLD_TIME_SECONDS)

    """
    Getters and setters
    """

    # Concrete methods for time properties
    def getLastHeatEnableTime(self) -> int:
        return self._getRecentTimeProp(CFG_LAST_HEAT_ENABLE_TIME)

    def setLastHeatEnableTime(self, time: int):
        self._setRecentTimeProp(CFG_LAST_HEAT_ENABLE_TIME, time)

    def getLastHeatDisableTime(self) -> int:
        return self._getRecentTimeProp(CFG_LAST_HEAT_DISABLE_TIME)

    def setLastHeatDisableTime(self, time: int):
        self._setRecentTimeProp(CFG_LAST_HEAT_DISABLE_TIME, time)

    def getLastCoolEnableTime(self) -> int:
        return self._getRecentTimeProp(CFG_LAST_COOL_ENABLE_TIME)

    def setLastCoolEnableTime(self, time: int):
        return self._setRecentTimeProp(CFG_LAST_COOL_ENABLE_TIME, time)

    def getLastCoolDisableTime(self) -> int:
        return self._getRecentTimeProp(CFG_LAST_COOL_DISABLE_TIME)

    def setLastCoolDisableTime(self, time: int):
        self._setRecentTimeProp(CFG_LAST_COOL_DISABLE_TIME, time)

    """
    Common utility methods
    """

    def _getRecentTimeProp(self, prop_name: str) -> int:
        if prop_name in self.recent_activity:
            return self.recent_activity[prop_name]
        return 0

    def _setRecentTimeProp(self, prop_name: str, time: int):
        self.recent_activity[prop_name] = time
        with open(self.file_name, 'w') as recent_activity:
            json.dump(self.recent_activity, recent_activity)
