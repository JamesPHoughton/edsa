
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
from django.contrib import admin
from edsa.log.models import Log, CommandResult

class LogAdmin(admin.ModelAdmin):
    def completed(self, obj):
        return (obj.end_time is not None)
    def runtime(self, obj):
        if obj.end_time:
            return obj.end_time - obj.start_time
        else:
            return 'N/A'   
    def machine_label(self, obj):
        return obj.machine.label
    def start_time_formatted(self, obj):
        return obj.start_time.strftime('%m/%d/%Y %I:%M:%S %p')
    
    list_display = ['label', 'tool', 'machine_label', 'start_time_formatted',  'completed', 'runtime']

admin.site.register(Log, LogAdmin)


admin.site.register(CommandResult)


