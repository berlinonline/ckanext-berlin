# coding: utf-8

import logging
import urllib2
import json


log = logging.getLogger(__name__)

class OrgRegister(object):
    """Dictionary-like interface to a group of organisations."""

    def __init__(self, org_url):
        self.load_orgs(org_url)

    
    def load_orgs(self, org_url):
        try:
            response = urllib2.urlopen(org_url)
            response_body = response.read()
        except Exception, inst:
            msg = "Couldn't connect to organisation list service %r: %s" % (org_url, inst)
            raise Exception(msg)

        try:
            data = json.loads(response_body)
        except Exception, inst:
            msg = "Couldn't read response from organisation list service %r: %s" % (org_url, inst)
            raise Exception(msg)

        self.orgs = data["@graph"]


    def __getitem__(self, key, default=Exception):
        for org in self.orgs:
            if key == org['@id']:
                return org
        if default != Exception:
            return default
        else:
            raise KeyError("Organisation not found: %s" % key)

    def get(self, key, default=None):
        return self.__getitem__(key, default=default)

    def keys(self):
        return [org['@id'] for org in self.orgs]

    def values(self):
        return self.orgs

    def items(self):
        return [(org['@id'], org) for org in self.orgs]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.orgs)

    def top_level_orgs(self):
        return [org for org in self.values() if org['pathDepth'] == 0]

    def org_hierarchy_list(self):
        tags = []
        self.descend_org_hierarchy(self.top_level_orgs(), tags, "fullName", False)
        return tags

    def descend_org_hierarchy(self, data, tags, name_property='longName', indent=True):
        for org in data:
            name = org[name_property]
            if indent:
                level = org['pathDepth']
                indentation = level * u'   '
                name = u"{0}{1}".format(indentation, name)
            tags.append({
                u'label': name,
                u'id': org['@id'].replace("verwaltung:", "http://daten.berlin.de/ref/organigramm/verwaltungen/")
            })
            if 'hasSubOrganization' in org:
                subOrgs = []
                for subOrg in org['hasSubOrganization']:
                    identifier = subOrg['@id']
                    subOrgs.append(self[identifier])
                self.descend_org_hierarchy(subOrgs, tags, name_property, indent)






