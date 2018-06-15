# coding: utf-8

import os
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)


class BerlinPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IConfigurer, inherit=False)

    # -------------------------------------------------------------------
    # Implementation IConfigurer
    # -------------------------------------------------------------------

    def update_config(self, config):  
        our_public_dir = os.path.join('theme', 'public')

        # overriding configuration fields:
        # set our local template and resource overrides
        toolkit.add_public_directory(config, our_public_dir)

        config['ckan.site_title'] = "Datenregister Berlin"
        config['ckan.locale_default'] = "de"
        config['ckan.locale_order'] = "de en"
        config['ckan.locales_offered'] = "de en"
        site_url = config.get('ckan.site_url', None)
        config['licenses_group_url'] = "{}{}".format(site_url, "/licenses/berlin-od-portal.json")

