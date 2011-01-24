
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
""" Helpful Form classes to add features to Django forms. """

from edsa.clients.models import Tool, Task

from django import forms

""" AutoDojoForm and AutoDojoModelForm: 
    These Form classes look over the fields that have been created in
    the constructor and try to turn their widgets into Dojo dijits.
"""
def update_fields(form):
    def update_widget(widget):
        attrs = widget.attrs
        if isinstance(widget, forms.TextInput):
            attrs['dojoType'] = 'dijit.form.TextBox'
        elif isinstance(widget, forms.SelectMultiple):
            attrs['dojoType'] = 'dijit.form.MultiSelect'
        elif isinstance(widget, forms.Select):
            attrs['dojoType'] = 'dijit.form.Select'
        elif isinstance(widget, forms.Textarea):
            attrs['dojoType'] = 'dijit.form.SimpleTextarea'
        widget.attrs = attrs
    for key in form.fields:
        update_widget(form.fields[key].widget)

class AutoDojoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AutoDojoForm, self).__init__(*args, **kwargs)
        update_fields(self)

class AutoDojoModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AutoDojoModelForm, self).__init__(*args, **kwargs)
        update_fields(self)

class HideableFieldsForm(AutoDojoForm):
    """ A Form class that provides functions to show and hide
        individual fields and lists of fields after they have been
        initialized.
    """

    def __init__(self, *args, **kwargs):
        super(HideableFieldsForm, self).__init__(*args, **kwargs)
        self._orig_widgets = {}

    def show_fields(self, field_names):
        for name in field_names:
            self.show_field(name)

    def show_field(self, field_name):
        if field_name in self._orig_widgets:
            self.fields[field_name].widget = self._orig_widgets[field_name]

    def hide_fields(self, field_names):
        for name in field_names:
            self.hide_field(name)
 
    def hide_field(self, field_name):
        if not isinstance(self.fields[field_name].widget, forms.HiddenInput):
            self._orig_widgets[field_name] = self.fields[field_name].widget
        self.fields[field_name].widget = forms.HiddenInput()
 
class AdjustableOnChangeForm(forms.Form):
    """ A Form class that allows you to specify the onChange parameters
        for fields by name by providing 'onchange_[field_name]'
        keyword arguments.  The goal is reduce the amount of code needed for
        this common operation.
    """
    
    def __init__(self, *args, **kwargs):

        onchange_dict = {}
        keys = kwargs.keys()
        for key in keys:
            if key.startswith('onchange_'):
                field_name = key[len('onchange_'):]
                onchange_dict[field_name] = kwargs[key]
                del kwargs[key]
            
        super(AdjustableOnChangeForm, self).__init__(*args, **kwargs)
        
        for field_name in onchange_dict:
            self.fields[field_name].widget.attrs['onChange'] = onchange_dict[field_name]

class ToolOrTaskForm(HideableFieldsForm):
    """ Many forms in EDSA rely on specifying either a Tool or a Task that
        can be executed.  They should subclass this Form class, which provides
        the appropriate fields and validation.
    """
    
    tool = forms.ModelChoiceField(queryset=Tool.objects.all(), required=False)
    task = forms.ModelChoiceField(queryset=Task.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ToolOrTaskForm, self).__init__(*args, **kwargs)
        #   Hide fields by default; they can be shown by subclasses
        self.hide_fields(['tool', 'task'])

    def clean(self):
        data = self.cleaned_data
        tool = data.get('tool')
        task = data.get('task')
        if tool and task:
            raise forms.ValidationError, 'Need either a tool or a task.'
        elif not tool and not task:
            raise forms.ValidationError, 'Need either a tool or a task, but not both.'
        return data
        
class SnatchArgumentsForm(AutoDojoForm):
    """ This is a Form class that allows nonstandard keyword arguments to be
        provided.  It pulls these out and stores them locally (prefixed
        with underscores)
       
        class MyForm(SnatchArgumentsForm):
            [form field definitions here]
            snatch_kwargs = ['param1', 'param2']
            #   After __init__, self._param1 contains what was in kwargs['param1'] 
    """
    def __init__(self, *args, **kwargs):
        for arg in self.__class__.snatch_kwargs:
            if arg in kwargs:
                setattr(self, '_' + arg, kwargs[arg])
                del kwargs[arg]
            else:
                setattr(self, '_' + arg, None)
        super(SnatchArgumentsForm, self).__init__(*args, **kwargs)
