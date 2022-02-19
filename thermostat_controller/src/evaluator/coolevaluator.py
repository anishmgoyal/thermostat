import circuit
import data
import evaluator.evaluator as evaluator
import logging


class CoolEvaluator(evaluator.Evaluator):
    @staticmethod
    def shouldDisableCooling(
            sensor: circuit.TemperatureSensor,
            settings: data.Settings,
            config: data.Config) -> bool:
        temp_c = sensor.getTemperature()
        target_temp = settings.getTargetCoolTemp()
        should_disable = target_temp is None
        if not should_disable:
            should_disable = \
                temp_c < float(target_temp) - config.getEpsilon()
        logging.debug("at {0:0.1f}C, target {1:0.1f}C, cool off: {2}".format(
            temp_c, target_temp, should_disable))
        return should_disable

    @staticmethod
    def shouldEnableCooling(
            sensor: circuit.TemperatureSensor,
            settings: data.Settings,
            config: data.Config) -> bool:
        temp_c = sensor.getTemperature()
        target_temp = settings.getTargetCoolTemp()
        should_enable = target_temp is not None
        if should_enable:
            should_enable = \
                temp_c >= float(target_temp) + config.getEpsilon()
        logging.debug("at {0:0.1f}C, target {1:0.1f}C, cool on: {2}".format(
            temp_c, target_temp, should_enable))
        return should_enable

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

        # If we can't make any changes, skip this iteration
        if not recent_activity.canToggle():
            logging.debug("Cannot toggle, skipping iteration")
            return

        # If we're in cool mode, first handle heating
        # mode, which might need to be disabled.
        if controller.is_heat_on:
            controller.shutDown()
            return

        temp_c = sensor.getTemperature()
        if temp_c is None:
            # Couldn't get temperature this iteration, so skip till
            # the next
            return

        curr_settings = super().getActiveSchedule(run_data, schedule)
        if controller.is_cool_on:
            # Check if we should turn cooling off.
            if self.shouldDisableCooling(temp_c, curr_settings, config):
                controller.shutDown()
        else:
            # Check if we should turn cooling on.
            if self.shouldEnableCooling(temp_c, curr_settings, config):
                controller.enableCool()
