# coding: utf-8

import os
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.plugins as lib_plugins
import ckan.lib.navl.validators as validators
import ckan.logic as logic
import ckan.logic.converters as converters
import ckan.lib.base as base
import validation as helper
from ckan.lib.navl.dictization_functions import DataError, StopOnError

log = logging.getLogger(__name__)

class BerlinPlugin(plugins.SingletonPlugin,
    lib_plugins.DefaultDatasetForm):

    log.debug("BerlinPlugin")

    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm, inherit=False)
# 
#     # Implementation IConfigurer
# 
    def update_config(self, config):  
        our_public_dir = os.path.join('theme', 'public')
        template_dir = os.path.join('theme', 'templates')

        # overriding configuration fields:
        # set our local template and resource overrides
        toolkit.add_public_directory(config, our_public_dir)
        toolkit.add_template_directory(config, template_dir)

        config['ckan.site_title'] = "Datenregister Berlin"
        config['ckan.site_logo'] = "/CKAN-logo.png"
        config['ckan.favicon'] = "http://datenregister.berlin.de/favicon.ico"

        # setting fix_partial_updates to True prevents empty lists from being stripped from dataset dicts,
        # which could cause errors in genshi calls such as package.resources in templates such as package_list.html
        config['ckan.fix_partial_updates'] = True
        

    # Implementation IDatasetForm

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

#     # def check_data_dict(self, data_dict, schema=None):
#     #     log.warning("check_data_dict")
#     #     
#     #     # make sure the dataset has been linked to a group
#     #     # one group set:
#     #     # { ... 'groups': [{'id': u'3cb2d53a-120d-4d2d-81f7-b79eaa3874f8'}], }
#     #     # two groups set ('eine-testgruppe' per checkbox, the other one per drop-down list):
#     #     # 'groups': [{'id': u'3cb2d53a-120d-4d2d-81f7-b79eaa3874f8',
#     #     #             'name': u'eine-testgruppe'},
#     #     #            {'id': u'3eb0e87a-11eb-4e00-bba6-35d35c92b105'}],
#     #     # two groups set (both per checkbox):
#     #     # 'groups': [{'id': u'3cb2d53a-120d-4d2d-81f7-b79eaa3874f8',
#     #     #             'name': u'eine-testgruppe'},
#     #     #            {'id': u'3eb0e87a-11eb-4e00-bba6-35d35c92b105',
#     #     #             'name': u'eine-zweite-testgruppe'}],
#     #     # no group set (unchecked checkboxes):
#     #     # 'groups': [{'name': u'eine-testgruppe'}, {'name': u'eine-zweite-testgruppe'}],
#     #     # no group set (nothing selected from drop-down list)
#     #     # 'groups': [],
#     #     if helper.at_least_one_id(data_dict['groups']):
#     #         log.debug("We have at least one group")
#     #     else:
#     #         log.debug("There is no group")
#     #         raise DataError('Der Datensatz muss mindestens einer Kategorie zugeordnet werden')
# 
    def form_to_db_schema(self):
        log.warning("form_to_db_schema")

        # get base dataset schema
        schema = logic.schema.form_to_db_package_schema()

        schema.update({
            # default fields
            'author': [helper.not_missing],
            'maintainer_email': [helper.not_missing, helper.validate_email_address, unicode],

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
        })
    
        return schema
    
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

    