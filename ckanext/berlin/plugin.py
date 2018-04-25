# coding: utf-8

import os
import logging
import ckan.model as model
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic.validators as validators
import validation as berlin_validators
import ckan.lib.plugins as lib_plugins
import ckan.logic as logic
# import ckan.logic.action.get as get
# import ckan.logic.action.update as update
# import ckan.logic.converters as converters
import ckan.lib.base as base

# import validation as helper
# from ckan.lib.navl.dictization_functions import DataError, StopOnError
from routes import url_for as url_for
from pylons import config

log = logging.getLogger(__name__)


class BerlinPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):

    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm)

    # -------------------------------------------------------------------
    # Implementation IConfigurer
    # -------------------------------------------------------------------

    def update_config(self, config):  
        our_public_dir = os.path.join('theme', 'public')
        template_dir = os.path.join('theme', 'templates')

        # overriding configuration fields:
        # set our local template and resource overrides
        toolkit.add_public_directory(config, our_public_dir)

        config['ckan.site_title'] = "Datenregister Berlin"
        config['ckan.locale_default'] = "de"
        config['ckan.locale_order'] = "de en"
        config['ckan.locales_offered'] = "de en"
        site_url = config.get('ckan.site_url', None)
        port = 80
        url_parts = site_url.split(":")
        if len(url_parts) > 2:
            port = url_parts[2]
        config['licenses_group_url'] = "http://localhost:{}{}".format(port, "/licenses/berlin-od-portal.json")


    # -------------------------------------------------------------------
    # Implementation ITemplateHelpers
    # -------------------------------------------------------------------

    def get_helpers(self):
        return {
            'berlin_dataset_type_mapping': dataset_type_mapping ,
            'berlin_type_mapping_select_options': type_mapping_select_options ,
            'berlin_temporal_granularity_select_options': temporal_granularity_select_options ,
            'berlin_geo_granularity_select_options': geo_granularity_select_options ,
            'berlin_geo_coverage_select_options':
                geo_coverage_select_options ,
            'berlin_state_mapping': state_mapping ,
            'berlin_user_orgs': organizations_for_user ,
            'berlin_is_sysadmin': is_sysadmin ,
        }

    # -------------------------------------------------------------------
    # Implementation IDatasetForm
    # -------------------------------------------------------------------
    
    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(BerlinPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(BerlinPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def _modify_package_schema(self, schema):
        schema.update({
            'username': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'berlin_type': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'berlin_source': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'date_released': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'date_updated': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'attribution_text': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')                
            ]
        })
        schema.update({
            'temporal_granularity': [
                toolkit.get_validator('ignore_missing'),
                # TODO: add validation
                # berlin_validators.contained_in_enum,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'temporal_coverage_from': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'temporal_coverage_to': [
                toolkit.get_validator('ignore_missing'),
                berlin_validators.isodate_notime,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'geographical_granularity': [
                toolkit.get_validator('ignore_missing'),
                # TODO: add validation
                # berlin_validators.contained_in_enum,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'geographical_coverage': [
                toolkit.get_validator('ignore_missing'),
                # TODO: add validation
                # berlin_validators.contained_in_enum,
                toolkit.get_converter('convert_to_extras')
            ]
        })
        return schema

    def show_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(BerlinPlugin, self).show_package_schema()
        schema.update({
            'username': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'berlin_type': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('not_missing')
            ]
        })
        schema.update({
            'berlin_source': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('not_missing')
            ]
        })
        schema.update({
            'date_released': [
                toolkit.get_converter('convert_from_extras'),
                berlin_validators.isodate_notime,
                toolkit.get_validator('not_missing')
            ]
        })
        schema.update({
            'date_updated': [
                toolkit.get_converter('convert_from_extras'),
                berlin_validators.isodate_notime,
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'attribution_text': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'temporal_granularity': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'temporal_coverage_from': [
                toolkit.get_converter('convert_from_extras'),
                berlin_validators.isodate_notime,
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'temporal_coverage_to': [
                toolkit.get_converter('convert_from_extras'),
                berlin_validators.isodate_notime,
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'geographical_granularity': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        schema.update({
            'geographical_coverage': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        return schema

