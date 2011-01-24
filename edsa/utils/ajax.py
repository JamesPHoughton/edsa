
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
import simplejson as json

class AjaxHandler(object):
    """ Helper class for Ajax operations.
        Performs common tasks and then hands off to your subclass's
        methods based on the supplied command.
    """

    #   Handles GET requests for now
    def handle(self, request, extra):
        data = {}
        for key in request.GET:
            data[str(key)] = str(request.GET[key])
        
        #   Strip extra part from path
        modified_path = request.path[:(len(request.path) - len(extra))]
        temp_context = {'request': {'path': modified_path}}
        
        required_keys = ['command', 'forms', 'target']
        for key in required_keys:
            if key not in data:
                raise Exception, 'Ajax update request submitted with no %s' % key

        #   Get request metadata
        command = data['command']
        targets = json.loads(data['target'])
        default_target = targets['default']
        form_data_dict = json.loads(data['forms'])
        
        #   Populate forms
        #   TODO: allow regular expression matching in FORM_MAPPING
        form_mapping = self.__class__.FORM_MAPPING
        form_dict = {}
        for key in form_data_dict:
            for match in form_mapping:
                if key.startswith(match):
                    form_dict[key] = form_mapping[match](form_data_dict[key], request.FILES)
        
        #   Stash data
        self.temp_context = temp_context
        self.form_dict = form_dict
        self.form_data_dict = form_data_dict
        self.targets = targets
        self.default_target = targets['default']
        
        #   Check for handler based on command
        if hasattr(self, command):
            return getattr(self, command)()
        else:
            raise Exception, 'No handler for command: %s' % command

