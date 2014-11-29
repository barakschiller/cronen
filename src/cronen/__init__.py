import threading
from datetime import datetime
import logging
import functools
import time
import json
from collections import namedtuple


import bottle
import schedule as schedule

log = logging.getLogger('cronen')

trigger = schedule

RunResult = namedtuple('RunResult', ('start_time', 'end_time', 'error'))

class ScheduledJob(object):
	"""
	A scheduled job with a web monitoring interface.
	:param func The job function (no parameters allowed, you can use functools to bind parameters).
	"""
	def __init__(self, name, func, trigger, error_handler):
		self.name = name
		self.func = func
		self.trigger = trigger
		self.last_run = RunResult('Never', 'Never', None)
		self.error_handler = error_handler

	def run(self):
		try:
			start_time = datetime.now()
			log.info('Running %s', self.name)
			self.func()
			end_time = datetime.now()
			self.last_run = RunResult(
				self.format_timestamp(start_time), 
				self.format_timestamp(end_time), 
				None)
		except Exception as e:
			log.exception('Error running job')
			
			end_time = datetime.now()
			self.last_run = RunResult(
				self.format_timestamp(start_time), 
				self.format_timestamp(end_time), 
				str(e))
			self.error_handler(self, e)
		finally:
			print 'Done running {}'.format(self.name)

	@staticmethod
	def format_timestamp(timestamp):
		return timestamp.isoformat()
	

class Cronen(object):

	@staticmethod
	def null_error_handler(job, exception):
		pass

	def __init__(self, port, error_handler=null_error_handler):
		"""
		:param port port to be used for web server
		:param error_handler error handler to be called in case of job failure
			function(ScheduledJob, Exception)
		"""
		self.port = port
		self.jobs = {}
		self.error_handler = error_handler


	def add_job(self, name, func, trigger):
		self.jobs[name] = ScheduledJob(name, func, trigger, self.error_handler)


	def start(self):
		"""
		Start scheduled task and web server. Call is blocking.
		"""
		self._start_scheduler()
		self._start_web_server()

	def _start_scheduler(self):
		for job in self.jobs.values():
			job.trigger.do(job.run)
		
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

		@bottle.route('/run/<name>')
		def web_run(name):
			logging.info('Running job {} manually'.format(name))
			self.jobs[name].run()
			
		@bottle.route('/status')
		def status():
			bottle.response.content_type = 'application/json'

			return json.dumps(
					{job.name:self.run_result_to_dict(job.last_run) for job in self.jobs.values()}
				)

		bottle.run(host='localhost', port=self.port)

	@staticmethod
	def run_result_to_dict(run_result):
		return run_result._asdict()