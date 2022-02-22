MQTT_HOSTNAME = 'amg_thermostat_hub'
MQTT_TOPIC = '/house/amg_thermostat/events'

# Common event configs
CFG_EVENT_TYPE = "event_type"

# values for a configuration update event
EVENT_UPDATE_CONFIG = "update_configuration"
CFG_CONFIG_TYPE = "config_type"
CONFIG_TYPE_BASE = "config"
CONFIG_TYPE_RUNDATA = "rundata"
CONFIG_TYPE_SCHEDULE = "schedule"

# values for a sensor reading event
EVENT_SENSOR_READING = "sensor_reading"
CFG_SENSOR_ID = "sensor_id"
CFG_SENSOR_TYPE = "sensor_type"
CFG_SENSOR_VALUE = "sensor_value"
SENSOR_TYPE_TEMPERATURE = "temp"
SENSOR_TYPE_HUMIDITY = "humid"
