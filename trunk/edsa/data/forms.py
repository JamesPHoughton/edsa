
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
""" Forms for data models: units, variables, etc. """

from edsa.data.models import Variable, BaseUnit, DataValue, VarType
from edsa.clients.models import Tool, Task
from edsa.tags.models import DataCategory

from edsa.utils.forms import AutoDojoForm, AutoDojoModelForm, ToolOrTaskForm, SnatchArgumentsForm

from django import forms

class ValueChoiceField(forms.ModelChoiceField):
    """ This field is defined to provide a more concise string format
        for DataValues listed in a dropdown box.
    """
    def label_from_instance(self, obj):
        return u"%s" % obj.data

class SelectValueForm(SnatchArgumentsForm, ToolOrTaskForm):
    """ A form that allows selecting from a set of values that the
        variable (supplied as a keyword argument) has been bound to recently.
    """
    variable = forms.ModelChoiceField(queryset=Variable.objects.all(), widget=forms.HiddenInput)
    value = ValueChoiceField(queryset=DataValue.objects.all().order_by('-timestamp'))

    snatch_kwargs = ['variable']

    def __init__(self, *args, **kwargs):

        super(SelectValueForm, self).__init__(*args, **kwargs)
        
        if self._variable:
            self.fields['variable'].initial = self._variable
            #   Get 10 most recent distinct values
            #   TODO: Figure out approach to grouping like values that doesn't take N queries
            id_list = self._variable.datavalue_set.all().values_list('id', flat=True)
            reasonable_values = DataValue.objects.filter(id__in=id_list).values('_data').distinct()[:10]
            id_list = []
            for item in reasonable_values:
                id_list.append(DataValue.objects.filter(_data=item['_data']).order_by('-timestamp')[0].id)
            self.fields['value'].queryset = DataValue.objects.filter(id__in=id_list).order_by('-timestamp')
            self.fields['value'].initial = self._variable.latest_value()

class EditValueForm(ToolOrTaskForm):
    """ A form that allows providing a new values for the given variable
        (supplied as a keyword argument).
    """
    variable = forms.ModelChoiceField(queryset=Variable.objects.all(), widget=forms.HiddenInput)
    value = forms.CharField()
    category = forms.ModelChoiceField(queryset=DataCategory.objects.all())

    def __init__(self, *args, **kwargs):
        snatch_kwargs = ['variable']
        for arg in snatch_kwargs:
            if arg in kwargs:
                setattr(self, '_' + arg, kwargs[arg])
                del kwargs[arg]
            else:
                setattr(self, '_' + arg, None)
                
        super(EditValueForm, self).__init__(*args, **kwargs)
        
        if self._variable and not self.data:
            self.fields['variable'].initial = self._variable
            
        if self.data.has_key('variable'):
            self._variable = Variable.objects.get(id=self.data['variable'])
        
        if self._variable:
            backup_dict = self.fields['value'].__dict__
            self.fields['value'] = self._variable.varType.get_formfield()
            #   self.fields['value'].__dict__.update(backup_dict)
            self.fields['value'].initial = unicode(self._variable.current_data)

""" Straightforward ModelForm classes for Variable and Unit. """
class VariableForm(AutoDojoModelForm):

    def __init__(self, *args, **kwargs):
        super(VariableForm, self).__init__(*args, **kwargs)
        self.initial['varType'] = VarType.objects.get(label='Float')

    class Meta:
        model = Variable
        exclude = ('tags',)

class UnitForm(AutoDojoModelForm):
    class Meta:
        model = BaseUnit
