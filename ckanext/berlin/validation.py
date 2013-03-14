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

# return True if at least one element of the list data contains a key 'id'
def at_least_one_id(data):
    for item in data:
        if 'id' in item.keys():
            return True
    return False

# validator for fields that require a value
def not_missing(key, data, errors, context):

    value = data.get(key)
    
    if not value or value is missing:
        errors[key].append(_(u'Wert für ein Pflichtfeld fehlt'))
        raise StopOnError

# check if e-mail address seems correct
def validate_email_address(key, data, errors, context):

    value = data.get(key)
    
    if not re.match(email_pattern, value, re.IGNORECASE):
        errors[key].append(_(u'Dies scheint keine gültige E-Mail-Adresse zu sein'))
        raise StopOnError

# check date format
def validate_date(key, data, errors, context):

    value = data.get(key)

    try:
        date_object = datetime.strptime(value, date_pattern)
    except ValueError:
        errors[key].append(_('Datum bitte im Format JJJJ-MM-TT angeben'))
        raise StopOnError


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

