import os
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.plugins as lib_plugins
import ckan.lib.navl.validators as validators
import ckan.logic as logic
import ckan.logic.converters as converters
import ckan.lib.base as base

log = logging.getLogger(__name__)

class BerlinPlugin(plugins.SingletonPlugin,
	lib_plugins.DefaultDatasetForm):
	
	plugins.implements(plugins.IConfigurer, inherit=False)
	plugins.implements(plugins.IDatasetForm, inherit=False)

	def update_config(self, config):	
		our_public_dir = os.path.join('theme', 'public')
		template_dir = os.path.join('theme', 'templates')
		
		# overriding configuration fields:
		# set our local template and resource overrides
		toolkit.add_public_directory(config, our_public_dir)
		toolkit.add_template_directory(config, template_dir)
		
		config['ckan.site_title'] = "Datenregister Berlin"
		config['ckan.site_description'] = "CKAN - Die Datenzentrale"
		config['ckan.site_logo'] = "/CKAN-logo.png"
		config['ckan.favicon'] = "http://datenregister.berlin.de/favicon.ico"
		config['ckan.template_footer_end'] = '<div class="footer">Ein Service von Fraunhofer FOKUS.</div>'
        
	def package_types(self):
		# This plugin doesn't handle any special package types, it just
		# registers itself as the default (above).
	    return []

	def is_fallback(self):
		# Return True to register this plugin as the default handler for
		# package types not handled by any other IDatasetForm plugin.
	    return True