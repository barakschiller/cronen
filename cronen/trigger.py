from collections import namedtuple
import datetime
import threading
from abc import ABCMeta, abstractmethod


class Trigger(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.next_run = None
        self.lock = threading.RLock()

    def fire_manually(self, ts):
        with self.lock:
            self.next_run = ts

    def should_fire(self, ts):
        return ts >= self.next_run

    def reset(self, ts):
        with self.lock:
            self.next_run = self.calculate_next_run(ts)

    @abstractmethod
    def calculate_next_run(self, ts):
        pass


class DailyTrigger(Trigger):
    def __init__(self, hour=0, minute=0):
        super(DailyTrigger, self).__init__()
        self.time = datetime.time(hour=hour, minute=minute)

    def calculate_next_run(self, ts):
        """
        :type ts datetime
        """
        running_time_today = datetime.datetime.combine(ts.date(), self.time)
        if ts >= running_time_today:
            # today's run has already passed
            return running_time_today + datetime.timedelta(days=1)
        else:
            return running_time_today


class PeriodicTrigger(Trigger):
    def __init__(self, timedelta):
        super(PeriodicTrigger, self).__init__()
        self.timedelta = timedelta

    def calculate_next_run(self, ts):
        return ts + self.timedelta


class WeeklyTrigger(Trigger):
    _DayOfTheWeek = namedtuple('DayOfTheWeek', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    DAYS_OF_THE_WEEK = _DayOfTheWeek(*range(7))

    def __init__(self, day_of_the_week=0, hour=0, minute=0):
        super(WeeklyTrigger, self).__init__()
        self.day_of_the_week = day_of_the_week
        self.time = datetime.time(hour=hour, minute=minute)

    def calculate_next_run(self, ts):
        """
        :type ts datetime
        """
        n_days_before_target = self.day_of_the_week - ts.weekday()
        date_to_run_this_week = ts.date() + datetime.timedelta(days=n_days_before_target)
        running_time_this_week = datetime.datetime.combine(date_to_run_this_week, self.time)
        if ts >= running_time_this_week:
            # this week's run has already passed
            return running_time_this_week + datetime.timedelta(days=7)
        else:
            return running_time_this_week
