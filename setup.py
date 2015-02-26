#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='cronen',
      packages=find_packages(),
      install_requires=['bottle',],
      version='1.0',
      description='A mini cron library for python. Allows scheduling jobs on a single node and provides a simple web interface for monitoring and manual triggering.',
      author='Barak Schiller',
      author_email='bschiller@gmail.com',
      url='https://github.com/barakschiller/cronen',
      download_url='https://github.com/barakschiller/cronen/tarball/1.0',
      keywords=['cron'],
      )
