
def isValidNumberInRange(num, min, max):
    if not isinstance(num, (int, float)) or isinstance(num, bool):
        return False
    return min <= num <= max

def isValidIntInRange(num, min, max):
    if not isinstance(num, int) or isinstance(num, bool):
        return False
    return min <= num <= max
