
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
# Django settings for edsa project.

DEBUG = True

DATABASES = {'default': 
    {'ENGINE':  'django.db.backends.postgresql_psycopg2',
     'NAME':    'edsa_django',
     'HOST':    'edsa.aurorardc.aero',
     'PORT':    '5432',
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True

MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'ukx71x_0-k*l7y)q!_71cib1n(d6s74i#l%hu_mcg$yw%*%%d8'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'edsa.urls'


INSTALLED_APPS = (
#    'debug_toolbar',
    'django_extensions',
    'mptt',
    'feincms',
    'edsa.tags',
    'edsa.data',
    'edsa.clients',
    'edsa.log',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'south',
)

FEINCMS_ADMIN_MEDIA = '/feincms_media/'

ADMINS = (
    ('Michael Price', 'mprice@aurora.aero'),
)

# Include local overrides
from database_settings import *
DATABASES['default']['USER'] = DATABASE_USER
DATABASES['default']['PASSWORD'] = DATABASE_PASSWORD

from local_settings import *

MEDIA_ROOT = PROJECT_ROOT + '/media'
MANAGERS = ADMINS
TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    PROJECT_ROOT + 'templates',
    EDSA_TOOL_WORKDIR, 
)

DAEMON_ROOT = PROJECT_ROOT + '/edsa'
PYRO_LOOP_INTERVAL = 10.0

PYRO_SETTINGS = {'PYRO_LOGFILE': 'daemons.log',
                 'PYRO_TRACELEVEL': 3,
                 'PYRO_USER_TRACELEVEL': 3,
                 'PYRO_STDLOGGING': 1,
                 #  This has to be set as an environment variable, unfortunately.
                 #  'PYRO_STORAGE': PROJECT_ROOT + '/storage',
                 'PYRO_HOST': EDSA_IP_ADDRESS,
                 'PYRO_MULTITHREADED': 1,
                 'PYRO_BROKEN_MSGWAITALL': 1,
                 'PYRO_SOCK_KEEPALIVE': 0,
                }


