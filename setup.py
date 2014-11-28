#!/usr/bin/env python

from distutils.core import setup
import setuptools

setup(name='cronen',
      version='1.0',
      package_dir={'': 'src'},
      description='Micro cron library',
      author='Barak Schiller',
      author_email='bschiller@gmail.com',
      packages=setuptools.find_packages(where='src'),
     )
