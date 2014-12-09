cronen
======

A mini cron library for python. Able to run scheduled jobs and provide a mini-web interface for manual scheduling.


# Usage example

```python
import cronen
from datetime import timedelta

def my_func():
  print 'Hello, world!'
  
def foo():
  print 'bar'

cron = cronen.Cronen(port=12345)

# schedule a simple hello-world job every day at 20:30.
cron.add_job(
  name='hello-job',
  func=my_func,
  trigger=cronen.trigger.DailyTrigger(hour=20, minute=30)
)


# Schedule a simple foo-bar job every 10 minutes
cron.add_job(
  name='foo-bar',
  func=foo,
  trigger=cronen.trigger.PeriodicTrigger(timedelta(minutes=10))
)

cron.stat()
```
