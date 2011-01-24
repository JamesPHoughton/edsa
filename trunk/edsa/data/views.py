
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
""" Views for data models (Variable, DataValue, etc.) 

"""

from edsa.data.models import Variable

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse

import simplejson as json

def show_variables(request):
    context = {'variables': Variable.objects.all()}
    return render_to_response('data/variables.html', context)

def last_value(request):
    if 'id' in request.GET:
        context = {}
        try:
            var_id = request.GET.get('id')
            context['value'] = Variable.objects.get(id=var_id).current_data
            result_str = render_to_string('data/datavalue_single.html', context)
            if request.is_ajax():
                return HttpResponse(json.dumps({('value_%s_html' % var_id): result_str}))
            else:
                return render_to_response('data/datavalue_single.html', context)
        except:
            raise
            return HttpResponse('Error fetching value; perhaps no values have yet been bound to that variable.')
    else:
        #   I think this causes a 404
        return None
