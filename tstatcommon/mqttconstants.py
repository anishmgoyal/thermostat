from tstatcommon.constants import LOCAL_DEV_MODE

MQTT_HOSTNAME = 'amgthermostathub.local' if LOCAL_DEV_MODE else 'localhost'
MQTT_HUB_HOSTNAME = 'amgthermostathub.local' # hostname of main thermostat
MQTT_TOPIC = '/house/amg_thermostat/events'

# Common event configs
CFG_EVENT_TYPE = "event_type"

# Values for a configuration update event
EVENT_UPDATE_CONFIG = "update_configuration"
CFG_CONFIG_TYPE = "config_type"
CONFIG_TYPE_BASE = "config"
CONFIG_TYPE_RUNDATA = "rundata"
CONFIG_TYPE_SCHEDULE = "schedule"

# Values for a state change event
EVENT_STATE_CHANGE = "state_change"
CFG_STATE_CHANGE_HOSTNAME = "hostname"
CFG_STATE_CHANGE_MODE = "mode"
CFG_STATE_CHANGE_FAN = "fan"
STATE_CHANGE_MODE_OFF = "off"
STATE_CHANGE_MODE_HEATING = "heat"
STATE_CHANGE_MODE_COOLING = "cool"
STATE_CHANGE_FAN_AUTO = "auto"
STATE_CHANGE_FAN_ON = "on"

# Values for a sensor reading event
EVENT_SENSOR_READING = "sensor_reading"
CFG_SENSOR_ID = "sensor_id"
CFG_SENSOR_TYPE = "sensor_type"
CFG_SENSOR_VALUE = "sensor_value"
SENSOR_ID_MAIN_SENSOR = "amg_thermostat_main"
SENSOR_TYPE_TEMPERATURE = "temp"
SENSOR_TYPE_HUMIDITY = "humid"

# Should not be sent to MQTT. Instead, consumers should get this event as a
# first event to indicate that the consumer is connected
EVENT_CONSUMER_INIT = "consumer_init"
CONSUMER_INIT_VER = "service_version"

# Event that indicates reload of the management service
EVENT_SERVICE_START = "service_start"
