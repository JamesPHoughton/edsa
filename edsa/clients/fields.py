
__author__    = "Aurora Flight Sciences"
__date__      = "$DATE$"
__rev__       = "$REV$"
__license__   = "GPL v.3"
__copyright__ = """
This file is part of EDSA, the Extensible Dataset Architecture system
Copyright (c) 2010-2011 Aurora Flight Sciences Corp.

Work on EDSA was sponsored by NASA Dryden Flight Research Center
under 2009 STTR contract NNX10CF57P.

EDSA is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free 
Software Foundation; either version 3 of the License, or (at your option) 
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
"""
Custom fields for editing clients models.
"""

from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django import forms

#   Adapted from http://code.djangoproject.com/attachment/ticket/7406/json_inputs.patch
class JsonInputs(forms.Widget):

    def render(self, name, value, attrs=None):
        import simplejson
        if value is None: value = '{}'
        value = simplejson.loads(force_unicode(value))
        ret = ''
        index = 1
        if value and len(value) > 0:
            for key in value.keys():
                ret += 'Key %d: <input class="jsontextbox" type="text" name="json_key[]" value="%s"> Value %d: <input class="jsontextbox" type="text" name="json_value[]" value="%s"><br />' % (index, key, index, value[key])
            index += 1
        ret += 'Key %d: <input class="jsontextbox" type="text" name="json_key[]"> Value %d: <input class="jsontextbox" type="text" name="json_value[]">' % (index, index)
        return mark_safe(ret)

    def value_from_datadict(self, data, files, name):
        json = data.copy()
        if json.has_key('json_key[]') and json.has_key('json_value[]'):
            keys = json["json_key[]"]
            values = json["json_value[]"]
            if not isinstance(keys, list):
                keys = [keys]
            if not isinstance(values, list):
                values = [values]
            jsonDict = {}
            for (key, value) in map(None, keys, values):
                if len(key) > 0:
                    jsonDict[key] = value
            import simplejson
            text = simplejson.dumps(jsonDict)

        print 'JSON field retrieved: %s' % text
        return text
