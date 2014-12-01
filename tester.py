import cronen
from datetime import timedelta
import functools

import logging
logging.basicConfig()


def my_func(param):
    print '*** running the job *** : ' + param


def my_bad_func():
    print '*** running the bad job ***'
    raise Exception('Some problem')


def error_handler(*args):
    print 'Error handler: ' + str(args)

func = functools.partial(my_func, 'something')

c = cronen.Cronen(11111, error_handler=error_handler)

c.add_job('okjob', func, cronen.PeriodicTrigger(timedelta(seconds=3)))
c.add_job('badjob',my_bad_func, cronen.PeriodicTrigger(timedelta(seconds=10)))
c.start()