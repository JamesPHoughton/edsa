
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
""" EDSA Pyro client

This file instantiates a singleton instance of a Pyro client with the following
methods:
-   get_names() - get available Pyro objects
-   get_object(obj_name) - get Pyro object from a name supplied by get_names()

For a usage example, see Task.get_available() in edsa/clients/models.py.

"""

from edsa import settings
from edsa.settings import PYRO_SETTINGS

import Pyro
import Pyro.core
import Pyro.naming

class PyroManager(object):
    def __init__(self, *args, **kwargs):
        #   Apply Pyro settings
        for field in PYRO_SETTINGS:
            if not field.startswith('_'):
                setattr(Pyro.config, field, PYRO_SETTINGS[field])

        #   Start Pyro
        Pyro.core.initClient()

        self.locator = Pyro.naming.NameServerLocator()
        self.ns = self.locator.getNS()

    def get_names(self):
        #   Query the Pyro nameserver for all available objets
        return self.ns.flatlist()
        
    def get_object(self, obj_name):
        #   Obtain a proxy for an object on a remote machine.
        uri = self.ns.resolve(obj_name)
        return uri.getAttrProxy()

#   Singleton (per-process) instance of PyroManager
pyro_manager = PyroManager()

