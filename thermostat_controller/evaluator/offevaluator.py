import circuit
import evaluator.evaluator as evaluator
import logging
import tstatcommon.data as data


class OffEvaluator(evaluator.Evaluator):
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
        logging.debug("Thermostat is in off mode")
        controller.shutDown()
