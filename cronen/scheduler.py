import datetime
from collections import namedtuple
import logging

log = logging.getLogger('cronen.scheduler')


class Scheduler(object):
    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)
        now = datetime.datetime.now()
        job.trigger.reset(now)

    def run_pending(self):
        now = datetime.datetime.now()
        for job in self.jobs:
            job.run_if_needed(now)

    def schedule_now(self, job):
        now = datetime.datetime.now()
        job.schedule_once(now)


class ScheduledJob(object):
    State = namedtuple('State', ('running', 'start_time', 'end_time', 'error'))
    INITIAL_STATE = State(running=False, start_time='', end_time='', error=None)

    """
    A scheduled job with a web monitoring interface.
    :param func The job function (no parameters allowed, you can use functools to bind parameters).
    """
    def __init__(self, name, func, trigger, error_handler):
        self.name = name
        self.func = func
        self.trigger = trigger
        self.state = self.INITIAL_STATE
        self.error_handler = error_handler

    def _run(self):
        error = None
        log.info('Running %s', self.name)
        start_time = datetime.datetime.now()
        self.state = self.State(running=True, start_time=self.format_timestamp(start_time), end_time='', error=None)
        try:
            self.func()
        except Exception as e:
            log.exception('Job %s failed', self.name)
            error = e
            try:
                self.error_handler(self, e)
            except Exception:
                log.exception('Error handler failed')
        finally:
            end_time = datetime.datetime.now()
            log.info('Done running %s', self.name)
            self.state = self.State(
                running=False,
                start_time=self.format_timestamp(start_time),
                end_time=self.format_timestamp(end_time),
                error=str(error)
            )

    def run_if_needed(self, ts):
        if self.trigger.should_fire(ts):
            self._run()
            self.trigger.reset(ts)

    def schedule_once(self, ts):
        self.trigger.fire_manually(ts)

    @staticmethod
    def format_timestamp(timestamp):
        return timestamp.isoformat()