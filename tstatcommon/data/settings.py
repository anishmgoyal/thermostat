from tstatcommon.constants import MODE_OFF

CFG_SETTINGS = 'settings'
CFG_TARGET_COOL_TEMP = 'target_cool_temp'
CFG_TARGET_HEAT_TEMP = 'target_heat_temp'


class Settings(object):
    def __init__(self, settings):
        self.settings = settings

    def getTargetCoolTemp(self) -> int:
        if CFG_TARGET_COOL_TEMP in self.settings:
            return self.settings[CFG_TARGET_COOL_TEMP]
        else:
            return None

    def setTargetCoolTemp(self, temp: int):
        self.settings[CFG_TARGET_COOL_TEMP] = temp

    def getTargetHeatTemp(self) -> int:
        if CFG_TARGET_HEAT_TEMP in self.settings:
            return self.settings[CFG_TARGET_HEAT_TEMP]
        else:
            return None

    def setTargetHeatTemp(self, temp: int):
        self.settings[CFG_TARGET_HEAT_TEMP] = temp
