import os
from logging import getLogger

from genshi.filters.transform import Transformer

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IGenshiStreamFilter
from ckan.plugins import IRoutes

log = getLogger(__name__)


class berlinPlugin(SingletonPlugin):
    """This plugin demonstrates how a theme packaged as a CKAN
    extension might extend CKAN behaviour.

    In this case, we implement three extension interfaces:

      - ``IConfigurer`` allows us to override configuration normally
        found in the ``ini``-file.  Here we use it to specify the site
        title, and to tell CKAN to look in this package for templates
        and resources that customise the core look and feel.
      - ``IGenshiStreamFilter`` allows us to filter and transform the
        HTML stream just before it is rendered.  In this case we use
        it to rename "frob" to "foobar"
      - ``IRoutes`` allows us to add new URLs, or override existing
        URLs.  In this example we use it to override the default
        ``/register`` behaviour with a custom controller
    """
    implements(IConfigurer, inherit=True)
    implements(IGenshiStreamFilter, inherit=True)
    implements(IRoutes, inherit=True)

    def update_config(self, config):
        """This IConfigurer implementation causes CKAN to look in the
        ```public``` and ```templates``` directories present in this
        package for any customisations.

        It also shows how to set the site title here (rather than in
        the main site .ini file), and causes CKAN to use the
        customised package form defined in ``package_form.py`` in this
        directory.
        """
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        our_public_dir = os.path.join(rootdir, 'ckanext', 'berlin', 'theme', 'public')
        template_dir = os.path.join(rootdir, 'ckanext', 'berlin', 'theme', 'templates')
        # set our local template and resource overrides
        config['extra_public_paths'] = ','.join([our_public_dir,
                config.get('extra_public_paths', '')])
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])
        # set the title
        config['ckan.site_title'] = "Datenregister Berlin"
        config['ckan.site_description'] = "CKAN - Die Datenzentrale"
        # set the customised package form (see ``setup.py`` for entry point)
        # config['package_form'] = "example_form"
        #config['site_url'] = "http://datenregister.berlin.de"
        config['ckan.site_logo'] = "/CKAN-logo.png"
        config['ckan.favicon'] = "http://datenregister.berlin.de/favicon.ico"
        config['ckan.template_footer_end'] = '<div class="footer">Ein Service von Fraunhofer FOKUS.</div>'
#        config['ckan.default_roles.Package'] = {"visitor": ["reader"], "logged_in": ["reader"]}
#        config['ckan.default_roles.Group'] = {"visitor": ["reader"], "logged_in": ["reader"]}
#        config['ckan.default_roles.System'] = {"visitor": ["reader"], "logged_in": ["reader"]}
#        config['ckan.default_roles.AuthorizationGroup'] = {"visitor": ["reader"], "logged_in": ["reader"]}

    def before_map(self, map):
        """This IRoutes implementation overrides the standard
        ``/user/register`` behaviour with a custom controller.  You
        might instead use it to provide a completely new page, for
        example.
        
        Note that we have also provided a custom register form
        template at ``theme/templates/user/register.html``.
        """
        # Note that when we set up the route, we must use the form
        # that gives it a name (i.e. in this case, 'register'), so it
        # works correctly with the url_for helper::
        map.connect('/package/new', controller='ckanext.berlin.controller:PackageNew', action='new')
        map.connect('/package/edit/{id}', controller='ckanext.berlin.controller:PackageNew', action='edit')
        map.connect('/package/new-classic', controller='ckanext.berlin.controller:PackageNewClassic', action='new')
        map.connect('/package/edit-classic/{id}', controller='ckanext.berlin.controller:PackageNewClassic', action='edit')
        return map
    
    def after_map(self, map):
	return map

