import os

INSTALLATION_DIR = os.path.sep + \
    os.path.sep.join(['var', 'lib', 'thermostat', 'control'])
DATA_DIR = os.path.sep.join([INSTALLATION_DIR, 'data'])
CONFIG_FILE = os.path.sep.join([DATA_DIR, 'config.json'])
RECENT_ACTIVITY_FILE = os.path.sep.join([DATA_DIR, 'recent_activity.json'])
RUNDATA_FILE = os.path.sep.join([DATA_DIR, 'run_data.json'])
SCHEDULE_FILE = os.path.sep.join([DATA_DIR, 'schedule.json'])
