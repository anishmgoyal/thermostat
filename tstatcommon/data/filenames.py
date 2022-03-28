import os
from tstatcommon.constants import LOCAL_DEV_MODE


INSTALLATION_DIR = os.path.sep + \
    os.path.sep.join(['var', 'lib', 'thermostat'])
DATA_DIR = os.path.sep.join([INSTALLATION_DIR, 'data'])

if LOCAL_DEV_MODE:
    DATA_DIR = os.path.sep.join([os.getcwd(), '..', 'default_config'])

CONFIG_FILE = os.path.sep.join([DATA_DIR, 'config.json'])
RECENT_ACTIVITY_FILE = os.path.sep.join([DATA_DIR, 'recent_activity.json'])
RUNDATA_FILE = os.path.sep.join([DATA_DIR, 'run_data.json'])
SCHEDULE_FILE = os.path.sep.join([DATA_DIR, 'schedule.json'])
STATE_FILE = os.path.sep.join([DATA_DIR, 'state.json'])

def getSwapFile(file_name: str) -> str:
    return file_name + ".swp"
