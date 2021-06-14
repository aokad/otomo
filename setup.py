# -*- coding: utf-8 -*-
"""
$Id: setup.py 335 2018-03-23 10:39:06Z aokada $
"""

from setuptools import setup
from scripts.otomo import __version__

setup(name='otomo',
      version=__version__,
      description="On-premises GCAT Workflow Job Manager",
      long_description="""""",

      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
          # Indicate who your project is intended for
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',

          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      
      keywords='bioinformatics',
      author='Ai Okada',
      author_email='aokad@ncc.go.jp',
      url='https://github.com/aokad/ecsub.git',
      license='GPLv3',
      
      package_dir = {'': 'scripts'},
      packages=['otomo'],
      scripts=['otomo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'awscli',
          'boto3',
          'requests'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      package_data = {
      }
)
