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
