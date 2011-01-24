
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
from edsa.data.models import MeasurementSystem, PhysicalQuantity, BaseUnit, Unit, UnitExponent, UnitConversion, Variable, DataValue, Constraint, LimitConstraint, FileValue, FileInstance, VarType

class MeasurementSystemAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(MeasurementSystem, MeasurementSystemAdmin)

class PhysicalQuantityAdmin(admin.ModelAdmin):
    list_display = ['label']
admin.site.register(PhysicalQuantity, PhysicalQuantityAdmin)

class BaseUnitAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'quantity_expressed', 'system']
admin.site.register(BaseUnit, BaseUnitAdmin)

class UnitAdmin(admin.ModelAdmin):
    def component_list(self, obj):
        comps_num = []
        comps_denom = []
        for comp in obj.expression.all():
            if comp.power_num == 0:
                break
            elif comp.power_denom:
                comps_num.append('%s^(%s/%s)' % (comp.unit.symbol, comp.power_num, comp.power_denom))
            elif comp.power_num > 0:
                if comp.power_num == 1:
                    comps_num.append('%s' % comp.unit.symbol)
                else:
                    comps_num.append('%s^%s' % (comp.unit.symbol, comp.power_num))
            else:
                if comp.power_num == -1:
                    comps_denom.append('%s' % comp.unit.symbol)
                else:
                    comps_denom.append('%s^%s' % (comp.unit.symbol, -comp.power_num))
        if len(comps_denom) > 0:
            return '%s / %s' % (' '.join(comps_num), ' '.join(comps_denom))
        else:
            return ' '.join(comps_num)
    list_display = ['symbol', 'name', 'component_list', 'quantity_expressed', 'system']
admin.site.register(Unit, UnitAdmin)

admin.site.register(UnitExponent)

class UnitConversionAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_unit', 'dest_unit', 'ratio', 'offset']
admin.site.register(UnitConversion, UnitConversionAdmin)

class VariableAdmin(admin.ModelAdmin):
    def tag_list(self, obj):
        return ', '.join(obj.tags.all().values_list('label', flat=True))
    list_display = ['label', 'description', 'unit', 'tag_list']
    readonly_fields = ['current_data']
admin.site.register(Variable, VariableAdmin)

class DataValueAdmin(admin.ModelAdmin):
    def tag_list(self, obj):
        return ', '.join(obj.tags.all().values_list('label', flat=True))
    def variable_symbol(self, obj):
        return obj.variable.label
    def variable_units(self, obj):
        return obj.variable.unit.symbol
    exclude = ['_data', 'tags']
    readonly_fields = ['data']
    list_display = ['id', 'variable_symbol', 'category', 'namespace', 'data', 'variable_units', 'supplier', 'timestamp', 'tag_list']
admin.site.register(DataValue, DataValueAdmin)

admin.site.register(FileValue)

admin.site.register(FileInstance)

class LimitConstraintAdmin(admin.ModelAdmin):
    def variable_list(self, obj):
        return u', '.join(obj.variables.all().values_list('label', flat=True))
    list_display = ['id', 'variable_list', 'min_values', 'max_values']
admin.site.register(LimitConstraint, LimitConstraintAdmin)

admin.site.register(VarType)

