import circuit
import controlmqtt
import logging
import tstatcommon
from tstatcommon import data, mqttconstants


class Evaluator(object):
    def evaluate(
            self,
            mqtt_client: controlmqtt.ControlMQTTClient,
            config: data.Config,
            controller: circuit.HVACController,
            recent_activity: data.RecentActivity,
            run_data: data.RunData,
            schedule: data.Schedule,
            sensor: circuit.TemperatureSensor):
        # common logic for updating sensor data in clients
        base_ev = {
            mqttconstants.CFG_EVENT_TYPE:
                mqttconstants.EVENT_SENSOR_READING,
            mqttconstants.CFG_SENSOR_ID:
                mqttconstants.SENSOR_ID_MAIN_SENSOR
        }
        
        temp_c = sensor.getTemperature()
        if temp_c is not None:
            mqtt_client.sendEvent({
                **base_ev,
                mqttconstants.CFG_SENSOR_TYPE:
                    mqttconstants.SENSOR_TYPE_TEMPERATURE,
                mqttconstants.CFG_SENSOR_VALUE: temp_c
            })
        
        humid = sensor.getHumidity()
        if humid is not None:
            mqtt_client.sendEvent({
                **base_ev,
                mqttconstants.CFG_SENSOR_TYPE:
                    mqttconstants.SENSOR_TYPE_HUMIDITY,
                mqttconstants.CFG_SENSOR_VALUE: humid
            })

        # common logic for checking the state of the fan
        if run_data.getFanEnabled() and not controller.is_fan_on:
            logging.debug("Turning the fan on")
            controller.enableFan()
        if not run_data.getFanEnabled() and controller.is_fan_on:
            logging.debug("Setting the fan to auto")
            controller.disableFan()

    def getActiveSchedule(self,
                          run_data: data.RunData,
                          schedule: data.Schedule):
        if run_data.getBehavior() == tstatcommon.constants.BEHAVE_SCHED:
            logging.debug("Looking for settings from schedule")
            active_schedule = schedule.getActiveEntry(run_data.getActiveMode())
            if active_schedule is not None:
                logging.debug("Active settings: {}".format(
                    active_schedule.settings))
                return active_schedule
            else:
                logging.debug("Failed to load settings from schedule")

        active_settings = run_data.getSettings()
        logging.debug("Active settings: {}".format(
            active_settings.settings))
        return active_settings
