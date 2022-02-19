import data.filenames as filenames
import data.settings as settings
import datetime
import json
import logging

CFG_ENTRIES = 'entries'
CFG_DAY_OF_WEEK = 'day_of_week'
CFG_START_HOUR = 'start_hour'
CFG_START_MINUTE = 'start_minute'
CFG_MODE = 'mode'
CFG_SETTINGS = 'settings'


class ScheduleEntry(object):
    def __init__(self, entry):
        self.entry = entry
        pass

    def getSettings(self):
        if CFG_SETTINGS in self.entry:
            return settings.Settings(self.entry[CFG_SETTINGS])
        else:
            return settings.Settings({})

    def getMode(self):
        if CFG_MODE in self.entry:
            return self.entry[CFG_MODE]
        return None

    def getDayOfWeek(self):
        if CFG_DAY_OF_WEEK in self.entry:
            return self.entry[CFG_DAY_OF_WEEK]

    def getStartHour(self):
        if CFG_START_HOUR in self.entry:
            return self.entry[CFG_START_HOUR]

    def getStartMinute(self):
        if CFG_START_MINUTE in self.entry:
            return self.entry[CFG_START_MINUTE]

    def isBeforeOrEqual(self, day: int, hour: int, minute: int) -> bool:
        return not self.isAfter(day, hour, minute)

    def isAfter(self, day: int, hour: int, minute: int) -> bool:
        if self.getDayOfWeek() > day:
            return True
        if self.getDayOfWeek() < day:
            return False
        if self.getStartHour() > hour:
            return True
        if self.getStartHour() < hour:
            return False
        if self.getStartMinute() > minute:
            return True
        return False

    def __str__(self):
        return str(self.entry)

    def __repr__(self):
        return str(self.entry)


class Schedule(object):
    def __init__(self):
        self.file_name = filenames.SCHEDULE_FILE
        self.entries_by_mode: dict[int, list[ScheduleEntry]] = {}
        self._loadSchedule()

    def getActiveEntry(self, mode: int) -> settings.Settings:
        if mode not in self.entries_by_mode:
            return None
        entries = self.entries_by_mode[mode]

        today = datetime.datetime.now()
        # If we're at the start of the week, we might need to steal the
        # settings from the end of last week
        if len(entries) > 0 and \
           entries[0].isAfter(today.weekday(), today.hour, today.minute):
            return entries[-1]

        lo, hi = 0, len(entries) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if entries[mid].isAfter(today.weekday(), today.hour, today.minute):
                hi = mid - 1
            elif mid < len(entries) - 1 and \
                    entries[mid + 1].isBeforeOrEqual(
                    today.weekday(), today.hour, today.minute):
                lo = mid + 1
            else:
                return entries[mid]
        return None

    def _loadSchedule(self):
        with open(self.file_name, 'r') as schedule:
            self.schedule = json.load(schedule)
        if CFG_ENTRIES in self.schedule:
            entries = [
                ScheduleEntry(entry) for entry in self.schedule[CFG_ENTRIES]]
        else:
            entries = []

        self.entries_by_mode = {}
        for entry in entries:
            if entry.getMode() is None or \
               entry.getDayOfWeek() is None or \
               entry.getStartHour() is None or \
               entry.getStartMinute() is None:
                continue

            mode = entry.getMode()
            if mode not in self.entries_by_mode:
                self.entries_by_mode[mode] = []
            self.entries_by_mode[mode].append(entry)

        for mode, entries in self.entries_by_mode.items():
            def entryKey(entry: ScheduleEntry):
                day = entry.getDayOfWeek()
                hour = entry.getStartHour()
                minute = entry.getStartMinute()
                return (day, hour, minute)
            self.entries_by_mode[mode] = sorted(entries, key=entryKey)

        logging.debug("Loaded schedule: {}".format(self.entries_by_mode))
