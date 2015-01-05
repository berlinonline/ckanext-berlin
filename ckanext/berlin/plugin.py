# coding: utf-8

import os
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.plugins as lib_plugins
import ckan.lib.navl.validators as validators
import ckan.logic as logic
import ckan.logic.action.get as get
import ckan.logic.action.update as update
import ckan.logic.converters as converters
import ckan.lib.base as base
import validation as helper
from ckan.lib.navl.dictization_functions import DataError, StopOnError

log = logging.getLogger(__name__)

class BerlinPlugin(plugins.SingletonPlugin,
    lib_plugins.DefaultDatasetForm):

    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.IActions, inherit=False)

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
        config['ckan.site_logo'] = "/CKAN-logo.png"
        config['ckan.favicon'] = "/favicon.ico"
        # config['ckan.fix_partial_updates'] = False

    # -------------------------------------------------------------------
    # Implementation IActions
    # -------------------------------------------------------------------
    
    def get_actions(self):
        
        log.debug("get_actions")
        
        def user_show(context, data_dict):
            
            log.debug("ckanext.berlin user_show")
            
            user_dict = get.user_show(context, data_dict)
            datasets = user_dict['datasets']
            for dataset in datasets:
                if 'resources' not in dataset:
                    log.debug("no resources in dataset, adding empty list")
                    dataset['resources'] = []
                if 'notes' not in dataset:
                    log.debug('no notes in dataset, adding empty string')
                    dataset['notes'] = u''
            
            return user_dict
        
        
        
        # def package_update_rest(context, data_dict):
        #     
        #     log.debug("ckanext.berlin package_update_rest")
        #     
        #     name = data_dict.get("name")
        #     current_data_dict = get.package_show(context, {'name_or_id': name})
        #     
        #     date_updated = current_data_dict.get('date_updated', None)
        #     
        #     data_dict['date_updated'] = date_updated
        #     
        #     context["extras_as_string"] = True
        #     return  update.package_update(context, data_dict)
        
        return {
            'user_show': user_show,
            # 'package_update_rest': package_update_rest,
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

    def form_to_db_schema(self):
        log.warning("form_to_db_schema")

        # get base dataset schema
        schema = logic.schema.form_to_db_package_schema()

        schema.update({
            # default fields
            'author': [helper.not_missing],
            'maintainer_email': [helper.not_missing, helper.validate_email_address, unicode],
            'license_id': [helper.not_missing],

            # custom fields
            'username': [validators.ignore_missing, unicode,
              converters.convert_to_extras],
            'date_released': [helper.not_missing, helper.validate_date, unicode,
              converters.convert_to_extras],
            'date_updated': [validators.ignore_empty, helper.validate_date, unicode,
              converters.convert_to_extras],
            'temporal_coverage-from': [validators.ignore_empty, helper.validate_date, unicode,
              converters.convert_to_extras],
            'temporal_coverage-to': [validators.ignore_empty, helper.validate_date, unicode,
              converters.convert_to_extras],
            'temporal_granularity': [validators.ignore_missing,
            converters.convert_to_tags('temporal_granularities')],
            'geographical_granularity': [validators.ignore_missing,
            converters.convert_to_tags('geographical_granularities')],
            'geographical_coverage': [validators.ignore_missing,
            converters.convert_to_tags('geographical_coverages')],
            'apps': [validators.ignore_missing, unicode,
              converters.convert_to_extras],
            'misc': [validators.ignore_missing, unicode,
              converters.convert_to_extras],
        })

        return schema

    def db_to_form_schema(self):
        log.warning("db_to_form_schema")
    
        # get base dataset schema
        schema = logic.schema.db_to_form_package_schema()
        
        # add our custom fields
        schema.update({
            'username': [converters.convert_from_extras,
              validators.ignore_missing],
            'date_released': [converters.convert_from_extras,
              validators.ignore_missing],
            'date_updated': [converters.convert_from_extras,
              validators.ignore_missing],
            'temporal_coverage-from': [converters.convert_from_extras,
              validators.ignore_missing],
            'temporal_coverage-to': [converters.convert_from_extras,
              validators.ignore_missing],
            'temporal_granularity': [converters.convert_from_tags('temporal_granularities'),
            validators.ignore_missing],
            'geographical_granularity': [converters.convert_from_tags('geographical_granularities'),
            validators.ignore_missing],
            'geographical_coverage': [converters.convert_from_tags('geographical_coverages'),
            validators.ignore_missing],
            'apps': [converters.convert_from_extras,
              validators.ignore_missing],
            'misc': [converters.convert_from_extras,
              validators.ignore_missing],
            # need to do something with "isopen" to prevent it from being stripped off the dataset dict during validation:
            'isopen': [validators.ignore_missing],
        })
    
        return schema

    
    # def form_to_db_schema_api_create(self):
    #     
    #     log.warning("form_to_db_schema_api_create")
    #     schema = self.form_to_db_schema()
    #     schema.update({
    #         'tags': logic.schema.default_tags_schema(),
    #         # 'extras': [validators.ignore],
    #     })
    #     return schema
    #     
    # def form_to_db_schema_api_update(self):
    # 
    #     log.warning("form_to_db_schema_api_update")
    #     schema = self.form_to_db_schema()
    #     schema.update({
    #         'tags': logic.schema.default_tags_schema(),
    #     })
    #     return schema
    # 

    def setup_template_variables(self, context, data_dict=None):
        lib_plugins.DefaultDatasetForm.setup_template_variables(self, context, data_dict)

        self.create_temporal_granularities()
        self.create_geographical_granularities()
        self.create_geographical_coverages()

        try:
            toolkit.c.temporal_granularities = logic.get_action('tag_list')(
            context, {'vocabulary_id': 'temporal_granularities'})
        except logic.NotFound:
            log.warning("no temporal_granularities vocab found, that should not happen!")
            toolkit.c.country_codes = None

        try:
            toolkit.c.geographical_granularities = logic.get_action('tag_list')(
            context, {'vocabulary_id': 'geographical_granularities'})
        except logic.NotFound:
            log.warning("no geographical_granularities vocab found, that should not happen!")
            toolkit.c.geographical_granularities = None

        try:
            toolkit.c.geographical_coverages = logic.get_action('tag_list')(
            context, {'vocabulary_id': 'geographical_coverages'})
        except logic.NotFound:
            log.warning("no geographical_coverages vocab found, that should not happen!")
            toolkit.c.geographical_coverages = None

    # -------------------------------------------------------------------

    def create_vocab(self, vocab_name, tags):
        user = logic.get_action('get_site_user')({
            'model': base.model, 'ignore_auth': True}, {})
        context = {
            'model': base.model, 
            'session': base.model.Session,
            'user': user['name']
        }

        try:
            data = {'id': vocab_name}
            logic.get_action('vocabulary_show')(context, data)
            log.info("'{name}' vocabulary already exists, skipping.".format(name=vocab_name))
        except logic.NotFound:
            log.info("Creating vocab '{name}'".format(name=vocab_name))
            data = {'name': vocab_name}
            vocab = logic.get_action('vocabulary_create')(context, data)
            for tag in tags:
                log.info(u"Adding tag {0} to vocab '".format(tag) + vocab_name + "'")
                data = {'name': tag, 'vocabulary_id': vocab['id']}
                logic.get_action('tag_create')(context, data)

    def create_temporal_granularities(self):
        vocab_name = 'temporal_granularities'
        tags = [
            u'Keine',
            u'5 Jahre',
            u'Jahr',
            u'Quartal',
            u'Monat',
            u'Woche',
            u'Tag',
            u'Stunde',
            u'Minute',
            u'Sekunde'
        ]
        self.create_vocab(vocab_name, tags)

    def create_geographical_granularities(self):
        vocab_name = 'geographical_granularities'
        tags = [
            u'Deutschland',
            u'Berlin',
            u'Bezirk',
            u'Ortsteil',
            u'Prognoseraum',
            u'Bezirksregion',
            u'Planungsraum',
            u'Block',
            u'Einschulbereich',
            u'Kontaktbereich',
            u'PLZ',
            u'Stimmbezirk',
            u'Quartiersmanagement',
            u'Wohnanlage',
            u'Wahlkreis'
        ]
        self.create_vocab(vocab_name, tags)

    def create_geographical_coverages(self):
        vocab_name = 'geographical_coverages'
        tags = [
            u'Adlershof',
            u'Alt-Hohenschönhausen',
            u'Alt-Treptow',
            u'Altglienicke',
            u'Baumschulenweg',
            u'Berlin',
            u'Biesdorf',
            u'Blankenburg',
            u'Blankenfelde',
            u'Bohnsdorf',
            u'Britz',
            u'Buch',
            u'Buckow',
            u'Charlottenburg',
            u'Charlottenburg-Nord',
            u'Dahlem',
            u'Deutschland',
            u'Friedenau',
            u'Friedrichsfelde',
            u'Friedrichshagen',
            u'Friedrichshain',
            u'Frohnau',
            u'Gatow',
            u'Gesundbrunnen',
            u'Gropiusstadt',
            u'Grunewald',
            u'Grünau',
            u'Hakenfelde',
            u'Halensee',
            u'Hansaviertel',
            u'Haselhorst',
            u'Heiligensee',
            u'Heinersdorf',
            u'Hellersdorf',
            u'Hermsdorf',
            u'Hohenschönhausen',
            u'Johannisthal',
            u'Karlshorst',
            u'Karow',
            u'Kaulsdorf',
            u'Kladow',
            u'Lichtenberg',
            u'Lichtenrade',
            u'Lichterfelde',
            u'Lübars',
            u'Mahlsdorf',
            u'Malchow',
            u'Mariendorf',
            u'Marienfelde',
            u'Marzahn',
            u'Marzahn-Hellersdorf',
            u'Mitte',
            u'Moabit',
            u'Märkisches Viertel',
            u'Müggelheim',
            u'Neu-Hohenschönhausen',
            u'Neukölln',
            u'Niederschöneweide',
            u'Niederschönhausen',
            u'Nikolassee',
            u'Oberschöneweide',
            u'Pankow ',
            u'Pankow',
            u'Plänterwald',
            u'Prenzlauer Berg',
            u'Rahnsdorf',
            u'Reinickendorf',
            u'Schmöckwitz',
            u'Schöneberg',
            u'Siemensstadt',
            u'Spandau',
            u'Staaken',
            u'Stadtrandsiedlung Malchow',
            u'Steglitz',
            u'Steglitz-Zehlendorf',
            u'Tegel',
            u'Tempelhof',
            u'Tempelhof-Schöneberg',
            u'Tiergarten',
            u'Treptow-Köpenick',
            u'Waidmannslust',
            u'Wannsee',
            u'Wartenberg',
            u'Wedding',
            u'Weißensee',
            u'Westend',
            u'Wilhelmsruh',
            u'Wilhelmstadt',
            u'Wilmersdorf',
            u'Wittenau',
            u'Zehlendorf'
        ]
        self.create_vocab(vocab_name, tags)

    