# coding: utf-8

import urllib, json

def tag_list_from_jsonld(jsonld_uri):
    """
    Reads a JSON_LD document from jsonld_uri.

    The following JSON_LD structure is assumed:
    {
      "@context": {
        ... context part ...
      },
      "@graph": [
        ... List of JSON objects which must contain a 'label'
        attribute. The returned list contains the values of 'label'. ...
      ]
    }
    """
    response = urllib.urlopen(jsonld_uri)
    data = json.loads(response.read())
    list = data['@graph']
    tags = []
    for tag in list:
        tags.append(tag['label'])
    return tags

def org_hierarchy_from_jsonld(jsonld_uri):
    """
    Reads a JSON_LD document from jsonld_uri.

    The following JSON_LD structure is assumed:
    {
      "@context": {
        ... context part ...
      } ,
      "@graph": {
        ... TODO ...
      }
    }
    """
    response = urllib.urlopen(jsonld_uri)
    data = json.loads(response.read())
    orgs = data["@graph"]
    tags = []
    descend_org_hierarchy(orgs, tags, 0)
    return tags


def descend_org_hierarchy(data, tags, level):
    for org in data:
        name = org['longName']
        indent = level * u'   '
        # if level > 0:
        #     name = u"∟" + name
        name = u"{0}{1}".format(indent, name)
        tags.append({
            u'label': name,
            u'id': org['@id'].replace("verwaltung:", "http://daten.berlin.de/ref/organigramm/verwaltungen/")
        })
        if 'hasSubOrganization' in org:
            subOrgs = org['hasSubOrganization']
            descend_org_hierarchy(subOrgs, tags, level + 1)



