import os
from logging import getLogger

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IDatasetForm

log = getLogger(__name__)

class BerlinPlugin(SingletonPlugin):
	
	implements(IConfigurer, inherit=True)
	implements(IDatasetForm, inherit=True)

	def update_config(self, config):	
		here = os.path.dirname(__file__)
		rootdir = os.path.dirname(os.path.dirname(here))
		our_public_dir = os.path.join(rootdir, 'ckanext', 'berlin', 'theme', 'public')
		template_dir = os.path.join(rootdir, 'ckanext', 'berlin', 'theme', 'templates')
		
		# overriding configuration fields:
		# set our local template and resource overrides
		config['extra_public_paths'] = ','.join([our_public_dir,
		        config.get('extra_public_paths', '')])
		config['extra_template_paths'] = ','.join([template_dir,
		        config.get('extra_template_paths', '')])
		
		config['ckan.site_title'] = "Datenregister Berlin"
		config['ckan.site_description'] = "CKAN - Die Datenzentrale"
		config['ckan.site_logo'] = "/CKAN-logo.png"
		config['ckan.favicon'] = "http://datenregister.berlin.de/favicon.ico"
		config['ckan.template_footer_end'] = '<div class="footer">Ein Service von Fraunhofer FOKUS.</div>'
        
	def package_form(self):
	    return 'package/new_package_form.html'

	def new_template(self):
	    return 'package/new.html'

	def comments_template(self):
	    return 'package/comments.html'

	def search_template(self):
	    return 'package/search.html'

	def read_template(self):
	    return 'package/read.html'

	def history_template(self):
	    return 'package/history.html'
	
	def package_types(self):
	    return ['dataset']

	def is_fallback(self):
	    return True