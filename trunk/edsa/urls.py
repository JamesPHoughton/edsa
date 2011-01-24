
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
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from edsa.views import home, upload_handler, tool_launcher, tool_editor, workflow_editor

from edsa import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^edsa/', include('edsa.foo.urls')),

    #   Home page
    (r'^$', home),

    #   App-specific views
    (r'^tasks_old/', include('edsa.clients.urls')),
    (r'^data/', include('edsa.data.urls')),
    (r'^logs/', include('edsa.log.urls')),

    #   Main landing views
    (r'^setup/$',tool_launcher),
    (r'^setup/([-a-zA-Z0-9_ ].*)$', tool_launcher), 
    (r'^edit/$', tool_editor), 
    (r'^edit/([-a-zA-Z0-9_ ].*)$', tool_editor), 
    (r'^workflow/$', workflow_editor), 
    (r'^workflow/([-a-zA-Z0-9_ ].*)$', workflow_editor), 
    
    #   Uploads
    (r'^upload/$', upload_handler),
    
    #   Django admin interface
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    #   Static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^feincms_media/(?P<path>.*)$', 'django.views.static.serve',
{'document_root': settings.FEINCMS_ADMIN_MEDIA_LOCATION, 'show_indexes': True}),

    #   Authentication
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
)

