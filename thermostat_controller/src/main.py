"""
This is the entry-point for the thermostat controller. This
service should continuously run in the background, and
control the HVAC system. It will periodically check for
updates in run-data, and apply them.
"""

import circuit
import data
import evaluator
import logging
import time
import tstatcommon

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

    while True:
        mode = run_data.getActiveMode()
        if mode == tstatcommon.constants.MODE_AUTO:
            curr_evaluator = evaluator.AutoEvaluator()
        elif mode == tstatcommon.constants.MODE_COOL:
            curr_evaluator = evaluator.CoolEvaluator()
        elif mode == tstatcommon.constants.MODE_HEAT:
            curr_evaluator = evaluator.HeatEvaluator()
        else:
            # MODE_OFF
            curr_evaluator = evaluator.OffEvaluator()

        evaluator.evaluate(
            config,
            controller,
            recent_activity,
            run_data,
            schedule,
            sensor)

        time.sleep(SLEEP_TIME)
