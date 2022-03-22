import calendar
import json

AUTO_NIGHT_COOL = 22.7778 # 73F
AUTO_NIGHT_HEAT = 20 # 68F
AUTO_DAY_COOL = 23.3332 # 74F
AUTO_DAY_HEAT = 20.5556 # 69F

COOL_NIGHT = 21.6667 # 71F
COOL_DAY = 22.7778 # 73F

HEAT_NIGHT = 21.1111 # 70F
HEAT_DAY = 22.2222 # 72F

MODE_COOL = 1
MODE_HEAT = 2
MODE_AUTO = 3

days = [
    calendar.SUNDAY,
    calendar.MONDAY,
    calendar.TUESDAY,
    calendar.WEDNESDAY,
    calendar.THURSDAY,
    calendar.FRIDAY,
    calendar.SATURDAY
]

def start_hour_for_day(day):
    if day == calendar.SUNDAY or day == calendar.SATURDAY:
        return 9
    return 6

def start_hour_for_night(day):
    if day == calendar.SUNDAY or day == calendar.SATURDAY:
        return 23
    return 21

def start_minute_for_night(day):
    if day == calendar.SUNDAY or day == calendar.SATURDAY:
        return 0
    return 30

entries = []
for day in days:
    entries.extend([{
        "mode": MODE_AUTO,
        "day_of_week": day,
        "start_hour": start_hour_for_day(day),
        "start_minute": 0,
        "settings": {
            "target_heat_temp": AUTO_DAY_HEAT,
            "target_cool_temp": AUTO_DAY_COOL
        }
    }, {
        "mode": MODE_AUTO,
        "day_of_week": day,
        "start_hour": start_hour_for_night(day),
        "start_minute": start_minute_for_night(day),
        "settings": {
            "target_heat_temp": AUTO_NIGHT_HEAT,
            "target_cool_temp": AUTO_NIGHT_COOL
        }
    }, {
        "mode": MODE_COOL,
        "day_of_week": day,
        "start_hour": start_hour_for_day(day),
        "start_minute": 0,
        "settings": {
            "target_cool_temp": COOL_DAY
        }
    }, {
        "mode": MODE_COOL,
        "day_of_week": day,
        "start_hour": start_hour_for_night(day),
        "start_minute": start_minute_for_night(day),
        "settings": {
            "target_cool_temp": COOL_NIGHT
        }
    }, {
        "mode": MODE_HEAT,
        "day_of_week": day,
        "start_hour": start_hour_for_day(day),
        "start_minute": 0,
        "settings": {
            "target_heat_temp": HEAT_DAY
        }
    }, {
        "mode": MODE_HEAT,
        "day_of_week": day,
        "start_hour": start_hour_for_night(day),
        "start_minute": start_minute_for_night(day),
        "settings": {
            "target_heat_temp": HEAT_NIGHT
        }
    }])

if __name__ == '__main__':
    with open('thermostat_controller/config/schedule.json', 'w') as sched:
        json.dump({
            "entries": entries
        }, sched, indent=4)
