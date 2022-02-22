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
            return False
    elif require_cool:
        return False

    if data.CFG_TARGET_HEAT_TEMP in settings:
        if not util_validators.isValidNumberInRange(
                settings[data.CFG_TARGET_HEAT_TEMP],
                15, # equiv to 60F
                27): # equiv to 80F
            return False
    elif require_heat:
        return False
    
    # Settings should have heat or cool, or both. If neither was
    # expected, the call to validate settings is not valid
    return require_heat or require_cool