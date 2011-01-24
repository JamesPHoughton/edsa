
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
EDSA custom form fields

These allow the submission of individual data values in formats that cannot be 
represented easily as a string.  For example, floating-point numbers can be
taken from a CharField but arrays and meshes cannot.
"""

from edsa.settings import EDSA_STORAGE_DIR

from django.template.loader import render_to_string
from django import forms

import numpy

class AjaxUploadWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        """ Renders the widget with the filename (relative to EDSA_STORAGE_DIR/uploads)
            as the value.
        """
        html = render_to_string('data/fileuploader.html', {'name': name, 'value': value})
        css = '<link rel="stylesheet" type="text/css" href="/media/styles/fileuploader.css" />\n'
        js = render_to_string('data/fileuploader.js', {'name': name, 'upload_url': '/upload/'})
        return css + html + js


class CustomizedArray(numpy.ndarray):
    def __unicode__(self):
        arraysize = ''
        for item in self.shape: 
            arraysize += str(item) + 'x'
        arraysize = arraysize[:-1]
        return u'Array of size %s' % arraysize

class ArrayField(forms.CharField):
    """ Behaves like a file field, except the uploaded file is converted to
        a numpy array and the file is removed.  """
    
    widget = AjaxUploadWidget
    
    def __init__(self, *args, **kwargs):
        super(ArrayField, self).__init__(*args, **kwargs)
        if 'help_text' not in kwargs:
            self.help_text = 'It should be a space-, tab-, or comma-separated text file containing only a numerical array.'
    
    def to_python(self, data):
        #   Get filename previously uploaded
        filename = '%s/uploads/%s' % (EDSA_STORAGE_DIR, data)
        
        #   Detect delimiter
        file = open(filename)
        top_row = file.readline()
        file.close()
        if ',' in top_row:
            delimiter = ','
        else:
            delimiter = None
            
        #   Load into array
        if delimiter:
            data = numpy.genfromtxt(filename, delimiter=delimiter)
        else:
            data = numpy.genfromtxt(filename)
        print 'Got data: %s' % data
        
        return CustomizedArray(data.shape, buffer=data)
        
    def clean(self, value):
        """ Override Django clean method to not run validators.  """
        value = self.to_python(value)
        self.validate(value)
        return value
        
    def validate(self, value):
        from django.forms import ValidationError
        
        if not isinstance(value, numpy.ndarray):
            print 'Problem value: %s' % value
            raise ValidationError('File did not contain array data')
        
        return value
