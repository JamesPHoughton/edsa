
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
from edsa.utils.rendering import render_to_response

from edsa.views.workflow import workflow_editor
from edsa.views.launcher import tool_launcher
from edsa.views.editor import tool_editor
from edsa.settings import EDSA_STORAGE_DIR

from django.http import HttpResponse

import simplejson as json
from datetime import datetime
import random

def home(request):
    from edsa import settings
    context = {'settings': settings}
    return render_to_response('home.html', context)

def handle_uploaded_file(f, field_name):
    filename = '%s_%s_%s' % (datetime.now().strftime('%Y%m%d%H%M%S'), field_name, ''.join(random.sample('0123456789', 6)))
    destination = open('%s/uploads/%s' % (EDSA_STORAGE_DIR, filename), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    print 'Saved file to %s/uploads/%s' % (EDSA_STORAGE_DIR, filename)
    return filename
    
def upload_handler(request):
    random.seed()
    
    #   Save files in upload area
    filename_dict = {}
    for key in request.FILES:
        filename_dict[key] = handle_uploaded_file(request.FILES[key], key)
    
    response_content = '<textarea>%s</textarea>' % json.dumps(filename_dict)
    return HttpResponse(response_content)
