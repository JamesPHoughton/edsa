
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
from edsa.clients.models import Country, StateProvince, Address, Biography, Institution, ContactInfo, Machine, Tool, Task, StimulusTask, PythonTool, CommandLineTool, RegisteredPythonModule, VariableProcessor
from edsa.log.models import Log

admin.site.register(Country)
admin.site.register(StateProvince)

class AddressAdmin(admin.ModelAdmin):
    def contact_name(self, obj):
        return obj.contactinfo.user.full_name
    def full_address(self, obj):
        return ', '.join([obj.address_line1, obj.address_line2])
    def state_code(self, obj):
        return obj.state_province.iso_code
    list_display = ['contact_name', 'full_address', 'city', 'state_code', 'country']
admin.site.register(Address, AddressAdmin)

admin.site.register(Biography)

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'url']
admin.site.register(Institution, InstitutionAdmin)

class ContactInfoAdmin(admin.ModelAdmin):
    def contact_name(self, obj):
        return obj.user.full_name
    list_display = ['contact_name', 'institution', 'department', 'last_updated']
admin.site.register(ContactInfo, ContactInfoAdmin)

class MachineAdmin(admin.ModelAdmin):
    def contact_name(self, obj):
        return obj.maintainer.full_name
    list_display = ['label', 'contact_name', 'ip_addr']
admin.site.register(Machine, MachineAdmin)

admin.site.register(RegisteredPythonModule)

class VariableProcessorAdmin(admin.ModelAdmin):
    def variable_list(self, obj):
        return u', '.join(obj.variables.all().values_list('label', flat=True))
    list_display = ['module', 'tool', 'processor_type', 'context', 'line_number', 'seq', 'variable_list']
admin.site.register(VariableProcessor, VariableProcessorAdmin)

class ToolAdmin(admin.ModelAdmin):
    def input_vars(self, obj):
        return u', '.join(obj.inputs.all().values_list('label', flat=True))
    def output_vars(self, obj):
        return u', '.join(obj.outputs.all().values_list('label', flat=True))
    def module_name(self, obj):
        return u'%s.%s' % (obj.module.module, obj.module.class_name)
    def machine_names(self, obj):
        limit = 3
        return u', '.join(obj.machines.all().values_list('label', flat=True)[:limit])

class PythonToolAdmin(ToolAdmin):
    list_display = ['label', 'maintainer', 'module_name', 'input_vars', 'output_vars', 'machine_names']
admin.site.register(PythonTool, PythonToolAdmin)

class CommandLineToolAdmin(ToolAdmin):
    list_display = ['label', 'maintainer', 'input_vars', 'output_vars', 'machine_names']
admin.site.register(CommandLineTool, CommandLineToolAdmin)

class TaskAdmin(admin.ModelAdmin):
    def num_dependencies(self, obj):
        return obj.dependencies.all().count()
    def execution_count(self, obj):
        qs = Log.objects.filter(task=obj)
        return '%s/%s' % (qs.filter(end_time__isnull=False).count(), qs.count())
    list_display = ['tool', 'num_dependencies', 'execution_count']
admin.site.register(Task, TaskAdmin)

class StimulusTaskAdmin(TaskAdmin):
    list_display = ['tool', 'module', 'num_dependencies', 'execution_count']
admin.site.register(StimulusTask, StimulusTaskAdmin)