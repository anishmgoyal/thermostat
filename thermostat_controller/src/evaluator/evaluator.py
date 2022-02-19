import circuit
import data
import logging
import tstatcommon


class Evaluator(object):
    def evaluate(
            self,
            config: data.Config,
            controller: circuit.HVACController,
            recent_activity: data.RecentActivity,
            run_data: data.RunData,
            schedule: data.Schedule,
            sensor: circuit.TemperatureSensor):
        # common logic for checking the state of the fan
        if run_data.getFanEnabled() and not controller.is_fan_on:
            controller.enableFan()
        if not run_data.getFanEnabled() and controller.is_fan_on:
            controller.disableFan()

    def getActiveSchedule(self,
                          run_data: data.RunData,
                          schedule: data.Schedule):
        if run_data.getBehavior() == tstatcommon.constants.BEHAVE_SCHED:
            active_schedule = schedule.getActiveEntry(run_data.getActiveMode())
            if active_schedule is not None:
                logging.debug("Active settings: {}".format(
                    active_schedule.settings))
                return active_schedule
        logging.debug("Active settings: {}".format(
            run_data.getSettings().settings))
        return run_data.getSettings()
