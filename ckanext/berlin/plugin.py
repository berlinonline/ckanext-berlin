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

# rather brutal implementation: if you're not logged in,
# you're not allowd to see anything. Not even the landing page
def berlin_site_read(context, data_dict=None):
    if context['user']:
        return { 'success': True }
    else:
        return { 'success': False }


def dataset_type_mapping():
    return {
      'datensatz': 'Datensatz', 
      'dokument': 'Dokument',
      'app': 'Anwendung'
    }

def author_select_options():
    return org_register().org_hierarchy_list()

# eventually, these values should come from a JSON API
# ids should be URIs, not just the label string
def geo_coverage_select_options():
    return [
        { u'id': u'Adlershof', u'label': u'Adlershof' } ,
        { u'id': u'Alt-Hohenschönhausen', u'label': u'Alt-Hohenschönhausen' } ,
        { u'id': u'Alt-Treptow', u'label': u'Alt-Treptow' } ,
        { u'id': u'Altglienicke', u'label': u'Altglienicke' } ,
        { u'id': u'Baumschulenweg', u'label': u'Baumschulenweg' } ,
        { u'id': u'Berlin', u'label': u'Berlin' } ,
        { u'id': u'Biesdorf', u'label': u'Biesdorf' } ,
        { u'id': u'Blankenburg', u'label': u'Blankenburg' } ,
        { u'id': u'Blankenfelde', u'label': u'Blankenfelde' } ,
        { u'id': u'Bohnsdorf', u'label': u'Bohnsdorf' } ,
        { u'id': u'Britz', u'label': u'Britz' } ,
        { u'id': u'Buch', u'label': u'Buch' } ,
        { u'id': u'Buckow', u'label': u'Buckow' } ,
        { u'id': u'Charlottenburg', u'label': u'Charlottenburg' } ,
        { u'id': u'Charlottenburg-Nord', u'label': u'Charlottenburg-Nord' } ,
        { u'id': u'Dahlem', u'label': u'Dahlem' } ,
        { u'id': u'Deutschland', u'label': u'Deutschland' } ,
        { u'id': u'Friedenau', u'label': u'Friedenau' } ,
        { u'id': u'Friedrichsfelde', u'label': u'Friedrichsfelde' } ,
        { u'id': u'Friedrichshagen', u'label': u'Friedrichshagen' } ,
        { u'id': u'Friedrichshain', u'label': u'Friedrichshain' } ,
        { u'id': u'Friedrichshain-Kreuzberg', u'label': u'Friedrichshain-Kreuzberg' } ,
        { u'id': u'Frohnau', u'label': u'Frohnau' } ,
        { u'id': u'Gatow', u'label': u'Gatow' } ,
        { u'id': u'Gesundbrunnen', u'label': u'Gesundbrunnen' } ,
        { u'id': u'Gropiusstadt', u'label': u'Gropiusstadt' } ,
        { u'id': u'Grunewald', u'label': u'Grunewald' } ,
        { u'id': u'Grünau', u'label': u'Grünau' } ,
        { u'id': u'Hakenfelde', u'label': u'Hakenfelde' } ,
        { u'id': u'Halensee', u'label': u'Halensee' } ,
        { u'id': u'Hansaviertel', u'label': u'Hansaviertel' } ,
        { u'id': u'Haselhorst', u'label': u'Haselhorst' } ,
        { u'id': u'Heiligensee', u'label': u'Heiligensee' } ,
        { u'id': u'Heinersdorf', u'label': u'Heinersdorf' } ,
        { u'id': u'Hellersdorf', u'label': u'Hellersdorf' } ,
        { u'id': u'Hermsdorf', u'label': u'Hermsdorf' } ,
        { u'id': u'Hohenschönhausen', u'label': u'Hohenschönhausen' } ,
        { u'id': u'Johannisthal', u'label': u'Johannisthal' } ,
        { u'id': u'Karlshorst', u'label': u'Karlshorst' } ,
        { u'id': u'Karow', u'label': u'Karow' } ,
        { u'id': u'Kaulsdorf', u'label': u'Kaulsdorf' } ,
        { u'id': u'Kladow', u'label': u'Kladow' } ,
        { u'id': u'Kreuzberg', u'label': u'Kreuzberg' } ,
        { u'id': u'Lichtenberg', u'label': u'Lichtenberg' } ,
        { u'id': u'Lichtenrade', u'label': u'Lichtenrade' } ,
        { u'id': u'Lichterfelde', u'label': u'Lichterfelde' } ,
        { u'id': u'Lübars', u'label': u'Lübars' } ,
        { u'id': u'Mahlsdorf', u'label': u'Mahlsdorf' } ,
        { u'id': u'Malchow', u'label': u'Malchow' } ,
        { u'id': u'Mariendorf', u'label': u'Mariendorf' } ,
        { u'id': u'Marienfelde', u'label': u'Marienfelde' } ,
        { u'id': u'Marzahn', u'label': u'Marzahn' } ,
        { u'id': u'Marzahn-Hellersdorf', u'label': u'Marzahn-Hellersdorf' } ,
        { u'id': u'Mitte', u'label': u'Mitte' } ,
        { u'id': u'Moabit', u'label': u'Moabit' } ,
        { u'id': u'Märkisches Viertel', u'label': u'Märkisches Viertel' } ,
        { u'id': u'Müggelheim', u'label': u'Müggelheim' } ,
        { u'id': u'Neu-Hohenschönhausen', u'label': u'Neu-Hohenschönhausen' } ,
        { u'id': u'Neukölln', u'label': u'Neukölln' } ,
        { u'id': u'Niederschöneweide', u'label': u'Niederschöneweide' } ,
        { u'id': u'Niederschönhausen', u'label': u'Niederschönhausen' } ,
        { u'id': u'Nikolassee', u'label': u'Nikolassee' } ,
        { u'id': u'Oberschöneweide', u'label': u'Oberschöneweide' } ,
        { u'id': u'Pankow', u'label': u'Pankow' } ,
        { u'id': u'Plänterwald', u'label': u'Plänterwald' } ,
        { u'id': u'Prenzlauer Berg', u'label': u'Prenzlauer Berg' } ,
        { u'id': u'Rahnsdorf', u'label': u'Rahnsdorf' } ,
        { u'id': u'Reinickendorf', u'label': u'Reinickendorf' } ,
        { u'id': u'Schmöckwitz', u'label': u'Schmöckwitz' } ,
        { u'id': u'Schöneberg', u'label': u'Schöneberg' } ,
        { u'id': u'Siemensstadt', u'label': u'Siemensstadt' } ,
        { u'id': u'Spandau', u'label': u'Spandau' } ,
        { u'id': u'Staaken', u'label': u'Staaken' } ,
        { u'id': u'Stadtrandsiedlung Malchow', u'label': u'Stadtrandsiedlung Malchow' } ,
        { u'id': u'Steglitz', u'label': u'Steglitz' } ,
        { u'id': u'Steglitz-Zehlendorf', u'label': u'Steglitz-Zehlendorf' } ,
        { u'id': u'Tegel', u'label': u'Tegel' } ,
        { u'id': u'Tempelhof', u'label': u'Tempelhof' } ,
        { u'id': u'Tempelhof-Schöneberg', u'label': u'Tempelhof-Schöneberg' } ,
        { u'id': u'Tiergarten', u'label': u'Tiergarten' } ,
        { u'id': u'Treptow-Köpenick', u'label': u'Treptow-Köpenick' } ,
        { u'id': u'Waidmannslust', u'label': u'Waidmannslust' } ,
        { u'id': u'Wannsee', u'label': u'Wannsee' } ,
        { u'id': u'Wartenberg', u'label': u'Wartenberg' } ,
        { u'id': u'Wedding', u'label': u'Wedding' } ,
        { u'id': u'Weißensee', u'label': u'Weißensee' } ,
        { u'id': u'Westend', u'label': u'Westend' } ,
        { u'id': u'Wilhelmsruh', u'label': u'Wilhelmsruh' } ,
        { u'id': u'Wilhelmstadt', u'label': u'Wilhelmstadt' } ,
        { u'id': u'Wilmersdorf', u'label': u'Wilmersdorf' } ,
        { u'id': u'Wittenau', u'label': u'Wittenau' } ,
        { u'id': u'Zehlendorf', u'label': u'Zehlendorf' } ,
    ]
    
def type_mapping_select_options():
    options = []
    for machine, human in dataset_type_mapping().items():
        options.append({ 'text': human, 'value': machine})
    return options

# eventually, these values should come from a JSON API
# ids should be URIs, not just the label string
def temporal_granularity_select_options():
    return [
        { u'id': u'Keine', u'label': u'Keine' } ,
        { u'id': u'5 Jahre', u'label': u'5 Jahre' } ,
        { u'id': u'Jahr', u'label': u'Jahr' } ,
        { u'id': u'Quartal', u'label': u'Quartal' } ,
        { u'id': u'Monat', u'label': u'Monat' } ,
        { u'id': u'Woche', u'label': u'Woche' } ,
        { u'id': u'Tag', u'label': u'Tag' } ,
        { u'id': u'Stunde', u'label': u'Stunde' } ,
        { u'id': u'Minute', u'label': u'Minute' } ,
        { u'id': u'Sekunde', u'label': u'Sekunde' } ,
    ]

# eventually, these values should come from a JSON API
# ids should be URIs, not just the label string
def geo_granularity_select_options():
    return [
        { u'id': u'Deutschland', u'label': u'Deutschland' } ,
        { u'id': u'Berlin', u'label': u'Berlin' } ,
        { u'id': u'Bezirk', u'label': u'Bezirk' } ,
        { u'id': u'Ortsteil', u'label': u'Ortsteil' } ,
        { u'id': u'Prognoseraum', u'label': u'Prognoseraum' } ,
        { u'id': u'Bezirksregion', u'label': u'Bezirksregion' } ,
        { u'id': u'Planungsraum', u'label': u'Planungsraum' } ,
        { u'id': u'Block', u'label': u'Block' } ,
        { u'id': u'Einschulbereich', u'label': u'Einschulbereich' } ,
        { u'id': u'Kontaktbereich', u'label': u'Kontaktbereich' } ,
        { u'id': u'PLZ', u'label': u'PLZ' } ,
        { u'id': u'Stimmbezirk', u'label': u'Stimmbezirk' } ,
        { u'id': u'Quartiersmanagement', u'label': u'Quartiersmanagement' } ,
        { u'id': u'Wohnanlage', u'label': u'Wohnanlage' } ,
        { u'id': u'Wahlkreis', u'label': u'Wahlkreis' } ,
        { u'id': u'Adresse', u'label': u'Adresse' } ,
    ]

def state_mapping():
    return {
        'active': u'veröffentlicht' ,
        'deleted': u'gelöscht'
    }


def organizations_for_user(user, permission='create_dataset'):
    '''Return a list of organizations that the given user has the specified
    permission for.
    '''
    context = {'user': user}
    data_dict = {'permission': permission}
    return logic.get_action('organization_list_for_user')(context, data_dict)

def is_sysadmin(user_name):
    user = model.User.get(unicode(user_name))
    return user.sysadmin


class BerlinPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):

    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IAuthFunctions)
    # plugins.implements(plugins.IActions, inherit=False)

    # -------------------------------------------------------------------
    # Implementation IConfigurer
    # -------------------------------------------------------------------

    def update_config(self, config):  
        our_public_dir = os.path.join('theme', 'public')
        template_dir = os.path.join('theme', 'templates')

        # overriding configuration fields:
        # set our local template and resource overrides
        toolkit.add_public_directory(config, our_public_dir)
        toolkit.add_template_directory(config, template_dir)

        config['ckan.site_title'] = "Datenregister Berlin"
        config['ckan.site_logo'] = "/images/berlin_open_data.png"
        config['ckan.favicon'] = "/favicon.ico"
        config['ckan.locale_default'] = "de"
        config['ckan.locale_order'] = "de en"
        config['ckan.locales_filtered_out'] = "ar bg ca cs_CZ da_DK el en_AU es fa_IR fi fr he hr hu id is it ja km ko_KR lt lv mn_MN ne nl no pl pt_BR pt_PT ro ru sk sl sq sr sr_Latn sv th tr uk_UA vi zh_CN zh_TW"
        config['licenses_group_url'] = "https://datenregister.berlin.de/licenses/berlin-od-portal.json"

        # authentication stuff:
        config['ckan.auth.anon_create_dataset'] = False
        config['ckan.auth.create_unowned_dataset'] = True
        config['ckan.auth.create_dataset_if_not_in_organization'] = True
        config['ckan.auth.user_create_groups'] = False
        config['ckan.auth.user_create_organizations'] = False
        config['ckan.auth.user_delete_groups'] = False
        config['ckan.auth.user_delete_organizations'] = False
        config['ckan.auth.create_user_via_api'] = False
        config['ckan.auth.create_user_via_web'] = False
        config['ckan.auth.roles_that_cascade_to_sub_groups'] = 'admin'


    # -------------------------------------------------------------------
    # Implementation ITemplateHelpers
    # -------------------------------------------------------------------

    def get_helpers(self):
        return {
            'berlin_dataset_type_mapping': dataset_type_mapping ,
            'berlin_type_mapping_select_options': type_mapping_select_options ,
            'berlin_author_select_options': author_select_options ,
            'berlin_temporal_granularity_select_options': temporal_granularity_select_options ,
            'berlin_geo_granularity_select_options': geo_granularity_select_options ,
            'berlin_geo_coverage_select_options':
                geo_coverage_select_options ,
            'berlin_state_mapping': state_mapping ,
            'berlin_user_orgs': organizations_for_user ,
            'berlin_is_sysadmin': is_sysadmin ,
        }

    # -------------------------------------------------------------------
    # Implementation IAuthFunctions
    # -------------------------------------------------------------------
    
    def get_auth_functions(self):
        return {
            'site_read': berlin_site_read ,
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

