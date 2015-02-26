import datetime
from mock import Mock
from nose.tools import assert_true, assert_equal

from cronen.scheduler import ScheduledJob

ANY_TIMESTAMP = datetime.datetime(2014, 1, 1)
ERROR_MESSAGE = 'error'


def raise_exception(*args):
    raise Exception(ERROR_MESSAGE)


class TestScheduler(object):
    def setup(self):
        self.always_fire_trigger = Mock()
        self.always_fire_trigger.should_fire.return_value = True

    def test_when_job_raised_exception_error_handler_called(self):
        mock_error_handler = Mock()
        job = ScheduledJob(name="job", func=raise_exception, trigger=self.always_fire_trigger,
                           error_handler=mock_error_handler)

        job.run_if_needed(ANY_TIMESTAMP)

        assert_true(mock_error_handler.called)
        assert_equal(job.state.error, ERROR_MESSAGE)

    def test_when_error_handler_raised_exception_it_is_caught(self):
        job = ScheduledJob(name="job", func=raise_exception, trigger=self.always_fire_trigger,
                           error_handler=raise_exception)

        job.run_if_needed(ANY_TIMESTAMP)

        assert_equal(job.state.error, ERROR_MESSAGE)