# coding: utf-8

import logging
import urllib2
import json


log = logging.getLogger(__name__)

class FeatureRegister(object):
    """Dictionary-like interface to a group of geographical features."""

    def __init__(self, feature_url):
        self.load_features(feature_url)

    
    def load_features(self, feature_url):
        try:
            response = urllib2.urlopen(feature_url)
            response_body = response.read()
        except Exception, inst:
            msg = "Couldn't connect to feature list service %r: %s" % (feature_url, inst)
            raise Exception(msg)

        try:
            data = json.loads(response_body)
        except Exception, inst:
            msg = "Couldn't read response from feature list service %r: %s" % (feature_url, inst)
            raise Exception(msg)

        self.features = data["@graph"]


    def __getitem__(self, key, default=Exception):
        for feature in self.features:
            if key == feature['@id']:
                return feature
        if default != Exception:
            return default
        else:
            raise KeyError("Feature not found: %s" % key)

    def get(self, key, default=None):
        return self.__getitem__(key, default=default)

    def keys(self):
        return [feature['@id'] for feature in self.features]

    def values(self):
        return self.features

    def items(self):
        return [(feature['@id'], feature) for feature in self.features]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.features)

    def top_level_features(self):
        return [feature for feature in self.values() if feature['@type'] == "berlin_geo:Land"]

    def feature_hierarchy_list(self):
        tags = []
        self.descend_feature_hierarchy(self.top_level_features(), tags)
        return tags

    def descend_feature_hierarchy(self, data, tags, name_property='label', indent=True):
        for feature in data:
            name = feature[name_property]
            feature_type = feature['@type'].replace('berlin_geo:', '')
            if indent:
                level = feature['pathDepth']
                indentation = level * u'   '
                name = u"{0}{1} ({2})".format(indentation, name, feature_type)
            tags.append({
                u'label': name,
                u'id': feature['@id'].replace("feature:", "http://daten.berlin.de/ref/geo/feature/")
            })
            if 'has_part' in feature:
                subFeatures = []
                for subFeature in feature['has_part']:
                    identifier = subFeature['@id']
                    subFeatures.append(self[identifier])
                self.descend_feature_hierarchy(subFeatures, tags, name_property, indent)






