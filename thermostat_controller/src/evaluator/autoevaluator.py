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
        if not recent_activity.canToggle():
            logging.debug("Cannot toggle heat or cooling, skipping iteration")
            return

        temp_c = sensor.getTemperature()
        if temp_c is None:
            logging.debug("No sensor data, skipping iteration")
            return

        logging.debug("Current temp: {0:0.1f}".format(temp_c))

        curr_settings = super().getActiveSchedule(run_data, schedule)
        if controller.is_heat_on:
            if heatevaluator.HeatEvaluator.shouldDisableHeat(
                    temp_c, curr_settings, config):
                logging.debug("Shutting down heater")
                controller.shutDown()

        elif controller.is_cool_on:
            if coolevaluator.CoolEvaluator.shouldDisableCooling(
                    temp_c, curr_settings, config):
                logging.debug("Shutting down cooler")
                controller.shutDown()

        elif heatevaluator.HeatEvaluator.shouldEnableHeat(
                temp_c, curr_settings, config):
            logging.debug("Enabling heater")
            controller.enableHeat()

        elif coolevaluator.CoolEvaluator.shouldEnableCooling(
                temp_c, curr_settings, config):
            logging.debug("Enabling cooler")
            controller.enableCool()
