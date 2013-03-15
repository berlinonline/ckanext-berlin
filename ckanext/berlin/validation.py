# coding: utf-8

import logging
import re
from ckan.lib.navl.dictization_functions import missing, StopOnError
from datetime import datetime
from pylons.i18n import _
from pprint import pprint
import sys, cStringIO, traceback

log = logging.getLogger(__name__)
date_pattern = "%Y-%m-%d"
email_pattern = "^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$"

error_key_mapping = {
    ('maintainer_email',): (u'Kontakt-Email',),
    ('date_released',): (u'Veröffentlichungsdatum',),
    ('date_updated',): (u'Aktualisierungsdatum',),
    ('temporal_coverage-from',): (u'Zeitraum von',),
    ('temporal_coverage-to',): (u'Zeitraum bis',),
    ('author',): (u'Veröffentlichende Stelle',),
    ('title',): (u'Titel',),
}

# return True if at least one element of the list data contains a key 'id'
def at_least_one_id(data):
    for item in data:
        if 'id' in item.keys():
            return True
    return False

# validator for fields that require a value
def not_missing(key, data, errors, context):

    value = data.get(key)
    key = convert_key(key)
    
    if not value or value is missing:
        add_error_message(key, errors, u'Wert für ein Pflichtfeld fehlt')
        raise StopOnError

# check if e-mail address seems correct
def validate_email_address(key, data, errors, context):

    value = data.get(key)
    key = convert_key(key)
    
    if not re.match(email_pattern, value, re.IGNORECASE):
        add_error_message(key, errors, u'Dies scheint keine gültige E-Mail-Adresse zu sein')
        raise StopOnError

# check date format
def validate_date(key, data, errors, context):

    value = data.get(key)
    key = convert_key(key)

    try:
        date_object = datetime.strptime(value, date_pattern)
    except ValueError:
        add_error_message(key, errors, u'Datum bitte im Format JJJJ-MM-TT angeben')
        raise StopOnError

def convert_key(key):
    if key in error_key_mapping:
        return error_key_mapping[key]
    else:
        return key

def add_error_message(key, errors, message):
    if key in errors:
        errors[key].append(_(message))
    else:
        errors[key] = [(_(message))]

def capture(func, *args, **kwargs):
    """Capture the output of func when called with the given arguments.

    The function output includes any exception raised. capture returns
    a tuple of (function result, standard output, standard error).
    """
    stdout, stderr = sys.stdout, sys.stderr
    sys.stdout = c1 = cStringIO.StringIO()
    sys.stderr = c2 = cStringIO.StringIO()
    result = None
    try:
        result = func(*args, **kwargs)
    except:
        traceback.print_exc()
    sys.stdout = stdout
    sys.stderr = stderr
    return (result, c1.getvalue(), c2.getvalue())

