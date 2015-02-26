import threading
import logging
from time import sleep
import json

import bottle
from cronen.scheduler import Scheduler, ScheduledJob

log = logging.getLogger('cronen')


def null_error_handler(job, exception):
    pass

class Cronen(object):

    def __init__(self, port, error_handler=null_error_handler):
        """
        :param port port to be used for web server
        :param error_handler error handler to be called in case of job failure
            function(ScheduledJob, Exception)
        """
        self.port = port
        self.jobs = {}
        self.error_handler = error_handler
        self.scheduler = Scheduler()
        self.scheduler_thread = None

    def add_job(self, name, func, trigger):
        job = ScheduledJob(name, func, trigger, self.error_handler)
        self.jobs[name] = job
        self.scheduler.add_job(job)

    def start(self):
        """
        Start scheduled task and web server. Call is blocking.
        """
        self._start_scheduler()
        self._start_web_server()

    def _start_scheduler(self):
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            name='Cronen Scheduler'
        )
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

    def _scheduler_loop(self):
        while True:
            self.scheduler.run_pending()
            sleep(1)

    def _start_web_server(self):

        @bottle.route('/run/<name>')
        def run(name):
            logging.info('Running job {} manually'.format(name))
            self.scheduler.schedule_now(self.jobs[name])

        @bottle.route('/status')
        def status():
            bottle.response.content_type = 'application/json'

            return json.dumps(
                {job.name: self.state_to_dict(job.state) for job in self.jobs.values()}
            )

        @bottle.route('/')
        def web_status():
            return bottle.template(WEB_STATUS_TEMPLATE, jobs=self.jobs.values())


        bottle.run(host='0.0.0.0', port=self.port)

    @staticmethod
    def state_to_dict(job_state):
        return job_state._asdict()



WEB_STATUS_TEMPLATE = """
<html>
<body>
<table id="jobs-table", border=1>
<tr>
    <th>Name</th>
    <th>Running?</th>
    <th>Start time</th>
    <th>End time</th>
    <th>Error</th>
    <th>Run</th>
</tr>
% for job in jobs:
<tr>
    <td>{{job.name}}</td>
    <td>{{job.state.running}}</td>
    <td>{{job.state.start_time}}</td>
    <td>{{job.state.end_time}}</td>
    <td>{{job.state.error}}</td>
    <td><button onclick="xmlhttp = new XMLHttpRequest(); xmlhttp.open('GET', 'run/{{job.name}}', true); xmlhttp.send();">Run</button></td>
</tr>
% end
</table>
</body>
</html>
"""
