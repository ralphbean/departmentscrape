from setuptools import setup, find_packages
import sys, os

version = '0.2a2'

setup(name='departmentscrape',
      version=version,
      description="little tool I use at work until we can get this done the right way",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='http://github.com/ralphbean/departmentscrape',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'twill',
          'ClientForm',
          'BeautifulSoup',
      ],
      )
