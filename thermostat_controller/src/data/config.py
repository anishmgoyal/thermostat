import data.filenames as filenames
import json

CFG_THERMOSTAT_EPSILON = 'thermostat_epsilon'


class Config(object):
    def __init__(self):
        self.file_name = filenames.CONFIG_FILE
        with open(self.file_name, 'r') as settings:
            self.settings = json.load(settings)

    def getEpsilon(self) -> float:
        """ Gets the threshold above / below a target temperature
            where the thermostat should be enabled (celsius) """
        if CFG_THERMOSTAT_EPSILON in self.settings:
            return self.settings[CFG_THERMOSTAT_EPSILON]
        DEFAULT_EPSILON = 0.5
        return DEFAULT_EPSILON
