# coding: utf-8

import logging
import re
from ckan.lib.navl.dictization_functions import missing, StopOnError
from datetime import datetime
from pylons.i18n import _

log = logging.getLogger(__name__)
date_pattern = "%Y-%m-%d"
email_pattern = "^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$"

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

