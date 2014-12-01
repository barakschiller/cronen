from mock import Mock
from nose.tools import assert_true, assert_equal

from scheduler import ScheduledJob


ERROR_MESSAGE = 'error'
def test_when_job_raised_exception_error_handler_called():

    def raise_exception():
        raise Exception(ERROR_MESSAGE)

    mock_trigger = Mock()
    mock_trigger.should_fire.return_value = True
    mock_error_handler = Mock()

    job = ScheduledJob(name="job", func=raise_exception, trigger=mock_trigger, error_handler=mock_error_handler)
    job.run_if_needed(None)

    assert_true(mock_error_handler.called)
    assert_equal(job.last_run.error, ERROR_MESSAGE)