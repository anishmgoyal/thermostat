import circuit
import data
import evaluator.coolevaluator as coolevaluator
import evaluator.evaluator as evaluator
import evaluator.heatevaluator as heatevaluator
import logging


class AutoEvaluator(evaluator.Evaluator):
    def evaluate(
            self,
            config: data.Config,
            controller: circuit.HVACController,
            recent_activity: data.RecentActivity,
            run_data: data.RunData,
            schedule: data.Schedule,
            sensor: circuit.TemperatureSensor):
        super().evaluate(
            config, controller, recent_activity, run_data, schedule, sensor)

        # We need to be able to do one of these two things to do anything useful
        # in this mode
        if not recent_activity.canToggleCool() and \
           not recent_activity.canToggleHeat():
            logging.debug("Cannot toggle heat or cooling, skipping iteration")
            return

        temp_c = sensor.getTemperature()
        if temp_c is None:
            logging.debug("No sensor data, skipping iteration")
            return

        logging.debug("Current temp: {0:0.1f}".format(temp_c))

        curr_settings = super().getActiveSchedule(run_data, schedule)
        if controller.is_cool_on:
            # Check if we should disable cooling
            if not recent_activity.canToggleCool():
                logging.debug("Cooling is on, and not changeable")
                return

            if coolevaluator.CoolEvaluator.shouldDisableCooling(
                    sensor, curr_settings, config):
                logging.debug("Shutting down cooler")
                controller.shutDown()

        elif controller.is_heat_on:
            # Check if we should disable heating
            if not recent_activity.canToggleHeat():
                logging.debug("Heating is on, and not changeable")
                return

            if heatevaluator.HeatEvaluator.shouldDisableHeat(
                    temp_c, curr_settings, config):
                logging.debug("Shutting down heater")
                controller.shutDown()

        elif recent_activity.canToggleCool() and \
                coolevaluator.CoolEvaluator.shouldEnableCooling(
                sensor, curr_settings, config):
            logging.debug("Enabling cooler")
            controller.enableCool()

        elif recent_activity.canToggleHeat() and \
                heatevaluator.HeatEvaluator.shouldEnableHeat(
                sensor, curr_settings, config):
            logging.debug("Enabling heater")
            controller.enableHeat()
