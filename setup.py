#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='cronen',
      version='1.0',
      description='Micro cron library',
      author='Barak Schiller',
      author_email='bschiller@gmail.com',
      packages=find_packages(),
      install_requires=[
            'bottle',
            ]
     )
