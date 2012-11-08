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
		
		toolkit.c.temporal_granularities = [
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
		
		toolkit.c.geographical_granularities = [
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
		
		toolkit.c.geographical_coverages = [
			u'Berlin',
			u'Marzahn-Hellersdorf',
			u'Mitte',
			u'Neukölln',
			u'Pankow ',
			u'Reinickendorf',
			u'Spandau',
			u'Steglitz-Zehlendorf',
			u'Tempelhof-Schöneberg',
			u'Treptow-Köpenick',
			u'Adlershof',
			u'Alt-Hohenschönhausen',
			u'Alt-Treptow',
			u'Altglienicke',
			u'Baumschulenweg',
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
			u'Grünau',
			u'Grunewald',
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
			u'Märkisches Viertel',
			u'Marzahn',
			u'Mitte',
			u'Moabit',
			u'Müggelheim',
			u'Neu-Hohenschönhausen',
			u'Neukölln',
			u'Niederschöneweide',
			u'Niederschönhausen',
			u'Nikolassee',
			u'Oberschöneweide',
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
			u'Tegel',
			u'Tempelhof',
			u'Tiergarten',
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
	