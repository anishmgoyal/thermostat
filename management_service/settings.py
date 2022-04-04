from main import app
from tstatcommon import data
import util_validators

MIN_ALLOWED_TEMP_DIFF = 2.2  # in celsius, 4 in fahremheit


def roundSettings(settings):
    """ Rounds all temperatures in settings to one decimal place """
    if data.CFG_TARGET_HEAT_TEMP in settings:
        settings[data.CFG_TARGET_HEAT_TEMP] = \
            round(settings[data.CFG_TARGET_HEAT_TEMP], 1)

    if data.CFG_TARGET_COOL_TEMP in settings:
        settings[data.CFG_TARGET_COOL_TEMP] = \
            round(settings[data.CFG_TARGET_COOL_TEMP], 1)


def validateSettings(settings,
                     require_heat=False,
                     require_cool=False):
    if data.CFG_TARGET_COOL_TEMP in settings:
        if not util_validators.isValidNumberInRange(
                settings[data.CFG_TARGET_COOL_TEMP],
                15,  # equiv to 60F
                27):  # equiv to 80F
            app.logger.info('cooling is out of range')
            return False
    elif require_cool:
        app.logger.info('settings is missing cooling')
        return False

    if data.CFG_TARGET_HEAT_TEMP in settings:
        if not util_validators.isValidNumberInRange(
                settings[data.CFG_TARGET_HEAT_TEMP],
                15,  # equiv to 60F
                27):  # equiv to 80F
            app.logger.info('heating is out of range')
            return False
    elif require_heat:
        app.logger.info('settings is missing heating')
        return False

    if require_heat and require_cool:
        # verify that we have the required gap
        diff = settings[data.CFG_TARGET_COOL_TEMP] - \
            settings[data.CFG_TARGET_HEAT_TEMP]

        # don't use absolute value; cool temp should be greater than heat temp
        if diff < MIN_ALLOWED_TEMP_DIFF:
            app.logger.info(
                'cooling / heat temps are too close: {}'.format(settings))
            return False

    if not require_heat and not require_cool:
        app.logger.info('neither heat nor cool was required, which is invalid')

    # Settings should have heat or cool, or both. If neither was
    # expected, the call to validate settings is not valid
    return require_heat or require_cool
