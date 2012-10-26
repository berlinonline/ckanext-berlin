from setuptools import setup, find_packages
import sys, os

version = '0.9'

setup(
	name='ckanext-berlin',
	version=version,
	description="Berlin Open Data Portal CKAN extension (custom theme and dataset form)",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Knud M\xc3\xb6ller',
	author_email='knud@datalysator.com',
	url='https://github.com/knudmoeller/ckanext-berlin',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.berlin'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	# myplugin=ckanext.berlin:PluginClass
	""",
)
