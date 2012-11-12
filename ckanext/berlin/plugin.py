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

log = logging.getLogger(__name__)

class BerlinPlugin(plugins.SingletonPlugin,
	lib_plugins.DefaultDatasetForm):
	
	plugins.implements(plugins.IConfigurer, inherit=False)
	plugins.implements(plugins.IDatasetForm, inherit=False)

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
			'Keine',
			'5 Jahre',
			'Jahr',
			'Quartal',
			'Monat',
			'Woche',
			'Tag',
			'Stunde',
			'Minute',
			'Sekunde'
		]
		self.create_vocab(vocab_name, tags)

	def create_geographical_granularities(self):
		vocab_name = 'geographical_granularities'
		tags = [
			'Berlin',
			'Bezirk',
			'Ortsteil',
			'Prognoseraum',
			'Bezirksregion',
			'Planungsraum',
			'Block',
			'Einschulbereich',
			'Kontaktbereich',
			'PLZ',
			'Stimmbezirk',
			'Quartiersmanagement',
			'Wohnanlage',
			'Wahlkreis'
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
	