"""
This is the entry-point for the thermostat controller. This
service should continuously run in the background, and
control the HVAC system. It will periodically check for
updates in run-data, and apply them.
"""

import circuit
import evaluator
import logging
import controlmqtt
import time
import tstatcommon
import tstatcommon.data as data

SLEEP_TIME = 2.0

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    logging.debug("Starting Thermostat")

    config = data.Config()
    recent_activity = data.RecentActivity()
    run_data = data.RunData()
    schedule = data.Schedule()

    controller = circuit.HVACController(recent_activity)
    sensor = circuit.TemperatureSensor()

    mqtt_client = controlmqtt.ControlMQTTClient(config, run_data, schedule)
    with mqtt_client:
        while True:
            mode = run_data.getActiveMode()
            logging.debug("Active mode: {}".format(mode))
            if mode == tstatcommon.constants.MODE_AUTO:
                logging.debug("Running in auto mode")
                curr_evaluator = evaluator.AutoEvaluator()
            elif mode == tstatcommon.constants.MODE_COOL:
                logging.debug("Running in cooling mode")
                curr_evaluator = evaluator.CoolEvaluator()
            elif mode == tstatcommon.constants.MODE_HEAT:
                logging.debug("Running in heating mode")
                curr_evaluator = evaluator.HeatEvaluator()
            else:
                # MODE_OFF
                logging.debug("Thermostat is off")
                curr_evaluator = evaluator.OffEvaluator()

            curr_evaluator.evaluate(
                mqtt_client,
                config,
                controller,
                recent_activity,
                run_data,
                schedule,
                sensor)

            time.sleep(SLEEP_TIME)
