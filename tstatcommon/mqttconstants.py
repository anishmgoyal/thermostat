MQTT_HOSTNAME = 'amg_thermostat_hub'
MQTT_TOPIC = '/house/amg_thermostat/events'

# Common event configs
CFG_EVENT_TYPE = "event_type"

# Values for a configuration update event
EVENT_UPDATE_CONFIG = "update_configuration"
CFG_CONFIG_TYPE = "config_type"
CONFIG_TYPE_BASE = "config"
CONFIG_TYPE_RUNDATA = "rundata"
CONFIG_TYPE_SCHEDULE = "schedule"

# Values for a sensor reading event
EVENT_SENSOR_READING = "sensor_reading"
CFG_SENSOR_ID = "sensor_id"
CFG_SENSOR_TYPE = "sensor_type"
CFG_SENSOR_VALUE = "sensor_value"
SENSOR_ID_MAIN_SENSOR = "amg_thermostat_main"
SENSOR_TYPE_TEMPERATURE = "temp"
SENSOR_TYPE_HUMIDITY = "humid"

# Event that indicates reload of the management service
EVENT_SERVICE_START = "service_start"
