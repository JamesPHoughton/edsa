
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
""" EDSA client daemon

This Python script creates an instance of a Pyro server that exports
remote objects for all tools present on the host.  It requires that a
Pyro nameserver is running somewhere on the network.  It should only be
run in one process at a time per host.

The singleton instance is called pyro_server.  To start a daemon, simply
import it: 
    from edsa.clients.daemon import pyro_server

Please ensure that the EDSA_MACHINE_NAME in your local_settings.py file 
matches any Tool entries stored in the database, if you would like to 
run them remotely through the Web interface.
"""

from edsa.settings import PYRO_SETTINGS, EDSA_MACHINE_NAME, PYRO_LOOP_INTERVAL

from edsa.data.models import FileInstance

from edsa.utils.subclass import get_subclass_instance
from edsa.utils.uris import generate_uri

from edsa.clients.models import Tool, VariableProcessor
from edsa.clients.remote import RemoteTool, RemoteFile, RemoteObject

import Pyro
import Pyro.core
import Pyro.naming

import cPickle as pickle
import threading
import hashlib
import os.path

class PyroServer(object):
    def __init__(self, *args, **kwargs):
        #   Apply Pyro settings
        for field in PYRO_SETTINGS:
            if not field.startswith('_'):
                setattr(Pyro.config, field, PYRO_SETTINGS[field])

        #   Get initial objects
        self.objects = []
        self.registered_objects = []
        self.compute_hash()

        #   Start the Pyro server
        self.run_server()

    def compute_hash(self):
        #   Stores and returns the MD5 hash of all local objects
        h = hashlib.new('md5')
        h.update(pickle.dumps(self.objects))
        self.object_hash = h.hexdigest()
        return self.object_hash

    def fetch_objects(self):
        #   Get tools and their associated data into local memory so it can be hashed
        tools = list(Tool.objects.filter(machines__label=EDSA_MACHINE_NAME))
        m2m_fields = [x.name for x in Tool._meta.many_to_many]
        for tool in tools:
            for field in m2m_fields:
                setattr(tool, '%s_data' % field, list(getattr(tool, field).all()))
                
        #   Get files
        files = list(FileInstance.objects.filter(machine__label=EDSA_MACHINE_NAME, exists=True))
        
        #   Get variable processors
        vps = list(VariableProcessor.objects.filter(tool__machines__label=EDSA_MACHINE_NAME))
        vps = list(VariableProcessor.objects.filter(tool__machines__label=EDSA_MACHINE_NAME))
        
        self.objects = tools + files + vps
        self.compute_hash()
        return self.objects

    def reload_objects(self):
        #   Clear nameserver entries
        for obj in self.registered_objects:
            self.daemon.disconnect(obj)
        self.registered_objects = []
        
        #   Supply available tools
        for obj in self.fetch_objects():
            obj = get_subclass_instance(obj)
            if isinstance(obj, Tool):
                ro = RemoteTool(obj)
            elif isinstance(obj, FileInstance):
                ro = RemoteFile(obj)
            else:
                #   We could do: ro = RemoteObject(obj) to register everything.
                #   But instead, just skip unsupported object types.
                continue
                
            self.registered_objects.append(ro)
            self.daemon.connect(ro, generate_uri(EDSA_MACHINE_NAME, obj))
            print 'Instantiated remotely accessible %s: %s' % (type(obj)._meta.object_name, obj)

    def run_server(self): 
        #   Start Pyro
        Pyro.core.initServer(banner=1)
        self.locator = Pyro.naming.NameServerLocator()
        self.ns = self.locator.getNS()
        self.daemon = Pyro.core.Daemon()
        self.daemon.useNameServer(self.ns)
        
        try:
            continue_loop = True
            while continue_loop:
                #   Keep track of things we want to notice changes to
                old_hash = self.object_hash
                self.fetch_objects()
                if self.object_hash != old_hash:
                    self.reload_objects()
                
                #   Check for new requests and wait for PYRO_LOOP_INTERVAL
                #   (default 10 sec) before checking for updated tools
                self.daemon.handleRequests(PYRO_LOOP_INTERVAL)
        except:
            #   If an exception is encountered, try to shut down cleanly.
            self.daemon.shutdown(True)
            raise
        
#   Singleton (per-process) instance of PyroServer
#	Defer calling to other code so it isn't executed in an import context
#	pyro_server = PyroServer()
pyro_server = PyroServer

