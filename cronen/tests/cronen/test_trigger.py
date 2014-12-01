from nose.tools import assert_equal
import datetime

from cronen.trigger import DailyTrigger


def test_daily_trigger_schedule_for_today():
    t = DailyTrigger(hour=8)
    early = datetime.datetime(2000, 1, 1, hour=1)
    next_run = t.calculate_next_run(early)
    assert_equal(datetime.datetime(2000, 1, 1, hour=8), next_run)


def test_when_too_late_daily_trigger_schedule_for_tomorrow():
    t = DailyTrigger(hour=8)
    late = datetime.datetime(2000, 1, 1, hour=10)
    next_run = t.calculate_next_run(late)
    assert_equal(datetime.datetime(2000, 1, 2, hour=8), next_run)


