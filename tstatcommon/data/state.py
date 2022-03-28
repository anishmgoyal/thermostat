import tstatcommon.data.filenames as filenames
import json
import os


class State(object):
    """
        Gets and sets information about current running state for the
        thermostat
    """

    def __init__(self):
        self.file_name = filenames.STATE_FILE

    def getState(self):
        with open(self.file_name, 'r') as state:
            return json.load(state)

    def setState(self, new_state):
        swap_file = filenames.getSwapFile(self.file_name)
        with open(swap_file, 'w') as state:
            json.dump(new_state, state, indent=4)
        os.replace(swap_file, self.file_name)
