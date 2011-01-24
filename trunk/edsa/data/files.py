
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

class BasicFile(object):
    def __init__(self, file, **kwargs):
        self.file = file
        
    def _get_contents(self):
        result = self.file.read()
        self.file.close()
        return result
    def _set_contents(self, new_contents):
        self.file.truncate()
        self.file.write(new_contents)
    contents = property(_get_contents, _set_contents)
    
    #   Attribute delegation if you want to use the file directly.
    def __getattr__(self, attr):
        if attr != 'file':
            return getattr(self.file, attr)
    
    def __unicode__(self):
        return self.file.name
