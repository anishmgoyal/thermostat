from main import app
from tstatcommon import data
import util_validators

def validateSettings(settings,
                     require_heat=False,
                     require_cool=False):
    if data.CFG_TARGET_COOL_TEMP in settings:
        if not util_validators.isValidNumberInRange(
                settings[data.CFG_TARGET_COOL_TEMP],
                15, # equiv to 60F
                27): # equiv to 80F
            app.logger.info('cooling is out of range')
            return False
    elif require_cool:
        app.logger.info('settings is missing cooling')
        return False

    if data.CFG_TARGET_HEAT_TEMP in settings:
        if not util_validators.isValidNumberInRange(
                settings[data.CFG_TARGET_HEAT_TEMP],
                15, # equiv to 60F
                27): # equiv to 80F
            app.logger.info('heating is out of range')
            return False
    elif require_heat:
        app.logger.info('settings is missing heating')
        return False

    if not require_heat and not require_cool:
        app.logger.info('neither heat nor cool was required, which is invalid')
    
    # Settings should have heat or cool, or both. If neither was
    # expected, the call to validate settings is not valid
    return require_heat or require_cool