import sys
from ckan.lib.base import request
from ckan.lib.base import c, g, h
from ckan.lib.base import model
from ckan.lib.base import render
from ckan.lib.base import _

from ckan.controllers.package import PackageController
class PackageNew(PackageController):
    package_form = 'package_form_berlin.html'


class PackageNewClassic(PackageController):
    package_form = 'package/new_package_form.html'



