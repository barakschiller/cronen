import threading
from datetime import datetime
import logging
import functools
import time


import bottle
import schedule

log = logging.getLogger('cronen')

class ScheduledJob(object):
	"""
	A scheduled job with a web monitoring interface.
	:param func The job function (no parameters allowed, you can use functools to bind parameters).
	"""
	def __init__(self, name, func, trigger):
		self.name = name
		self.func = func
		self.trigger = trigger
		self.last_run = (None, None, None)

	def run(self):
		try:
			start_time = datetime.now()
			log.info('Running %s', self.name)
			self.func()
			end_time = datetime.now()
			self.last_run = (start_time, end_time, None)
		except Exception as e:
			log.exception('Error running job')
			#TODO: add error email support?
			end_time = datetime.now()
			self.last_run = (start_time, end_time, e)

		finally:
			print 'Done running {}'.format(self.name)

	

class Cronen(object):
	def __init__(self, port):
		self.port = port
		self.jobs = {}

	def add_job(self, name, func, trigger):
		self.jobs[name] = ScheduledJob(name, func, trigger)


	def start(self):
		"""
		Start scheduled task and web server. Call is blocking.
		"""
		self._start_scheduler()
		self._start_web_server()

	def _start_scheduler(self):
		# TODO: add scheduling configuration
		for job in self.jobs.values():
			schedule.every(5).seconds.do(job.run)
		
		self.scheduler = threading.Thread(
			target=self._scheduler_loop,
			name='Cronen Scheduler'
			)
		self.scheduler.daemon = True
		self.scheduler.start()

	def _scheduler_loop(self):
		while True:
			schedule.run_pending()
			time.sleep(1)

	def _start_web_server(self):
		# setup routes
		@bottle.route('/run/<name>')
		def web_run(name):
			logging.info('Running job {} manually'.format(name))
			self.jobs[name].run()
			
		@bottle.route('/status')
		def status():
			return "\n".join(
				"Job: {}, last run: {}".format(j.name, j.last_run) for j in self.jobs.values()
				)

		bottle.run(host='localhost', port=self.port)