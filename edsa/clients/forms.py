
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
""" Forms for client models: tools, tasks, machines, etc. """

from django.db import models
from django import forms
from django.utils.safestring import mark_safe
from django.forms.formsets import formset_factory

from edsa.clients.models import EDSAUser, RegisteredPythonModule, Tool, PythonTool, CommandLineTool, Task, StimulusTask, Machine, VariableProcessor
from edsa.data.models import BaseUnit,Variable,DataValue,VarType,BaseUnit,PhysicalQuantity, MeasurementSystem
from edsa.log.models import Log

from edsa.clients.fields import JsonInputs
from edsa.utils.forms import AutoDojoForm, AutoDojoModelForm, HideableFieldsForm, AdjustableOnChangeForm, SnatchArgumentsForm, ToolOrTaskForm
from edsa.utils.subclass import get_subclass_instance

import pylab
import datetime


""" Forms that manipulate models that are not Tasks/Tools """

class RegisteredPythonModuleForm(AutoDojoModelForm):
    """ Straightforward ModelForm for entering a RegisteredPythonModule. """
    class Meta:
        model = RegisteredPythonModule


""" Forms that manipulate Tools """

class SelectToolForm(AdjustableOnChangeForm):
    tool = forms.ModelChoiceField(queryset=Tool.objects.all(), widget=forms.Select(attrs={'dojoType': "dijit.form.Select", 'onChange': "update_form('/edit/', 'select_tool_form', {default: 'pane_configure_tool', vars_in: 'pane_in_vars', vars_out: 'pane_out_vars', log: 'footer'}, 'select_tool');"}))

class CreateToolForm(forms.Form):
    tool_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'dojoType': "dijit.form.ValidationTextBox" ,'promptMessage': 'Name your tool!', 'required': "true", 'onChange': "ToolSave()"}))
    version = forms.CharField(label='Version', widget=forms.TextInput(attrs={'dojoType': "dijit.form.ValidationTextBox", 'promptMessage': 'Tool version or release', 'required':"true", 'onChange': "ToolSave()"}))

class RunToolForm(SnatchArgumentsForm, HideableFieldsForm):
    """ Collects information needed to execute a Tool, including what machine
        to run it on and where it falls in a sequence of Tool executions.
    """
    
    tool = forms.ModelChoiceField(queryset=Tool.objects.all(), widget=forms.HiddenInput)
    machine = forms.ModelChoiceField(queryset=Machine.objects.all())
    params = forms.CharField(required=False)
    seq = forms.IntegerField(widget=forms.HiddenInput, required=False)
    
    snatch_kwargs = ['tool', 'machines']
    
    def __init__(self, *args, **kwargs):
        super(RunToolForm, self).__init__(*args, **kwargs)
        
        if self._tool:
            self._tool = get_subclass_instance(self._tool)
            self.initial['tool'] = self._tool
            if isinstance(self._tool, PythonTool):
                self.initial['params'] = self._tool.module._default_params
            else:
                self.hide_field('params')
            if self._machines:
                self.fields['machine'].queryset = self._tool.machines.filter(label__in=self._machines)

class VariableSetForm(forms.Form):
    """ A polymorphic form that manages a set of variables associated with a tool.
        The form always shows you one blank field for entering a new variable.
        Fields for modifying variable selections are accompanied by a checkbox
        to delete that variable from the set.
    """
    direction = forms.ChoiceField(choices=(('in', 'in'), ('out', 'out')), widget=forms.HiddenInput)
    tool = forms.ModelChoiceField(queryset=Tool.objects.all(), widget=forms.HiddenInput)

    def _get_num_vars(self):
        match_txt = 'var_%s_' % self.direction
        keys = self.fields.keys()
        keys.sort()
        max_index = 0
        for key in self.fields:
            if key.startswith(match_txt):
                index = int(key[len(match_txt):])
                if index > max_index:
                    max_index = index
        return index
    num_vars = property(_get_num_vars)

    def get_variable_field(self, direction, index, update_str, var=None):
        if hasattr(var, 'id'):
            var_id = var.id
        else:
            var_id = ''
	VAR=Variable.objects.all()
        return forms.ModelChoiceField(label='%s variable %d' % (direction.title(), index), queryset=VAR.order_by('label'),widget=forms.Select(attrs={'dojoType':"dijit.form.Select", 'value': var_id, 'onChange': update_str}), initial=var, required=False)
        
    def get_delete_field(self, direction, index, update_str):
        return forms.NullBooleanField(initial=False, label='Delete variable %d?' % index, widget=forms.CheckboxInput(attrs={'dojotype':"dijit.form.CheckBox",'onChange': update_str}))

    def add_variable(self, var=None):
        direction = self.direction
        update_str = self.update_str
        count = self.num_vars
        
        if direction == 'in':
            self.tool.inputs.add(var)
        elif direction == 'out':
            self.tool.outputs.add(var)
        
        #   Set value of last field to the supplied variable
        self.fields['var_%s_%d' % (direction, count)] = self.get_variable_field(direction, count, update_str, var)
        #   Add "delete?" field after the last variable field 
        self.fields['delete_%s_%d' % (direction, count)] = self.get_delete_field(direction, count, update_str)
        #   Add and another variable field after that
        self.fields['var_%s_%d' % (direction, count + 1)] = self.get_variable_field(direction, count + 1, update_str)
        
        print 'Added variable %s' % var

    def dump_fields(self):
        print 'Dumping %d fields for %s VariableSetForm' % (self.num_vars, self.direction)
        for field in self.fields:
            print ' -> %s = %s' % (field, self.fields[field].initial)

    def __init__(self, *args, **kwargs):
        
        vars = []
        
        count = 0
        if len(args) >= 1:
            data = args[0]
            if 'tool' not in data or 'direction' not in data:
                raise Exception, 'VariableSetForm requires both tool and direction to be provided'
            tool = Tool.objects.get(id=data['tool'])
            direction = data['direction']
            
            #   Populate fields that were in existing data
            match_txt = 'var_%s_' % direction
            if direction == 'in':
                m2m_obj = tool.inputs
            elif direction == 'out':
                m2m_obj = tool.outputs
            #   print 'Clearing %s of %s' % (direction, tool)
            m2m_obj.clear()
            keys = data.keys()
            keys.sort()
            for key in keys:
                if key.startswith(match_txt):
                    delete_key = 'delete_%s_' % direction + str(count + 1)
                    #   print 'Checking against delete key %s' % delete_key
                    if delete_key not in data:
                        try:
                            #   print 'Adding %s: %s' % (key, Variable.objects.get(id=data[key]))
                            m2m_obj.add(data[key])
                            count += 1
                        except:
                            pass
                            #   print 'Error adding %s, skipping.' % key
                    else:
                        #   print 'Skipping %s since it was marked for deletion' % key
                        del data[delete_key]
                        del data[key]
                    
            #   print 'Count at end of parsing = %d; objects in m2m = %d' % (count, m2m_obj.count())
            
            #   Reset fields and rewrite data seen by Django form
            self.fields = {}
            args = list(args)
            args[0] = data
            
        else:
            if 'tool' not in kwargs or 'dir' not in kwargs:
                raise Exception, 'VariableSetForm requires both tool and dir keyword args if not provided'
            tool = kwargs['tool']
            del kwargs['tool']
            direction = kwargs['dir']
            del kwargs['dir']
            
        self.direction = direction
        self.tool = tool
        if direction == 'in':
            vars = tool.inputs.all()
            form_id = 'var_in_form'
            form_div_id = 'pane_input_vars'
        elif direction == 'out':
            vars = tool.outputs.all()
            form_id = 'var_out_form'
            form_div_id = 'pane_output_vars'
        else:
            raise Exception, 'Improper dir for VariableSetForm.  Choices are in, out'
        #   print 'Found %d existing variables.' % vars.count()
            
        form_div_id = 'pane_%s_vars' % direction

        super(VariableSetForm,self).__init__(*args, **kwargs)
        
        self.fields['tool'].initial = tool
        self.fields['direction'].initial = direction

        #   Populate fields
        count = 1
        update_str = "update_form('/edit/', '%s', '%s', 'update_%s_vars');" % (form_id, form_div_id, direction)
        self.update_str = update_str
        for var in vars:
            print 'Populating field for variable %d: %s' % (count, var)
            self.fields['var_%s_%d' % (direction, count)] = self.get_variable_field(direction, count, update_str, var)
            self.fields['delete_%s_%d' % (direction, count)] = self.get_delete_field(direction, count, update_str)
            count += 1
        self.fields['var_%s_%d' % (direction, count)] = self.get_variable_field(direction, count, update_str)
        self.data['var_%s_%d' % (direction, count)] = None
        
class ToolConfigForm(HideableFieldsForm):
    """ A polymorphic form which is used to configure either a PythonTool
        or a CommandLineTool.
    """

    #   The choice in this field determines which otherfields are needed to set up a tool.
    tool_type = forms.ChoiceField(choices=(('', '[Select one]'), ('python', 'Python tool'), ('cmdline', 'Command-line tool')), widget=forms.Select(attrs={'onChange': mark_safe('update_form(\'/edit/\', \'config_form\', \'pane_configure_tool\', \'set_tool_type\');')}))

    existing_tool = forms.ModelChoiceField(queryset=Tool.objects.all(), widget=forms.HiddenInput, required=False)

    #   Fields for Python tools
    PYTHONTOOL_FIELDS = ['rpm']
    rpm = forms.ModelChoiceField(label='Python module', queryset=RegisteredPythonModule.objects.all(), required=False)
    
    #   Fields for command-line tools
    COMMANDLINETOOL_FIELDS = ['commands']
    commands = forms.CharField(widget=forms.Textarea, required=False)
 
    #   Fields contributed by other forms
    OTHER_FIELDS = ['tool_name', 'tool_version', 'machines']
    machines = forms.ModelMultipleChoiceField(queryset=Machine.objects.all())
    tool_name = forms.CharField(widget=forms.HiddenInput)
    tool_version = forms.CharField()
 
    ALL_FIELDS = PYTHONTOOL_FIELDS + COMMANDLINETOOL_FIELDS + OTHER_FIELDS
 
    def __init__(self, *args, **kwargs):
    
        #   Extract type of tool from arguments
        type_of_tool = None
        if len(args) >= 1:
            data = args[0]
            if 'tool_type' in data:
                if data['tool_type'] == 'python': type_of_tool = PythonTool
                elif data['tool_type'] == 'cmdline': type_of_tool = CommandLineTool
               
        super(ToolConfigForm, self).__init__(*args, **kwargs)
        
        self.setup_tool_type(type_of_tool)

    def setup_tool_type(self, type_of_tool):
        #   Handle initial data
        if type_of_tool:
            if type_of_tool == PythonTool:
                self.fields['tool_type'].initial = 'python'
                self.hide_fields(ToolConfigForm.COMMANDLINETOOL_FIELDS)
            elif type_of_tool == CommandLineTool:
                self.fields['tool_type'].initial = 'cmdline'
                self.hide_fields(ToolConfigForm.PYTHONTOOL_FIELDS)
        else:
            #   Tool type has not yet been specified.
            self.hide_fields(ToolConfigForm.ALL_FIELDS)
            
    def load(self, tool):
        """ Populate form with information from an existing tool """
        
        tool = get_subclass_instance(tool)
        type_of_tool = type(tool)
        self.show_fields(ToolConfigForm.ALL_FIELDS)
        self.setup_tool_type(type_of_tool)
        if type_of_tool == PythonTool:
            self.fields['tool_type'].initial = 'python'
            self.fields['rpm'].initial = tool.module
        elif type_of_tool == CommandLineTool:
            self.fields['tool_type'].initial = 'cmdline'
            self.fields['commands'].initial = tool.client_cmd
        else:
            raise Exception, 'Unsupported tool type %s for ToolConfigForm.load()' % type_of_tool

        self.fields['existing_tool'].initial = tool
        self.fields['machines'].initial = tool.machines.all()
        self.fields['tool_name'].initial = tool.label
        self.fields['tool_version'].initial = tool.version

    def save(self, *args, **kwargs):
        """ Use data contained in the form to update or create a tool """
        
        data = self.cleaned_data
        
        #   Get or create desired tool
        if data['existing_tool']:
            tool = get_subclass_instance(data['existing_tool'])
        else:
            if data['tool_type'] == 'python':
                tool = PythonTool()
            elif data['tool_type'] == 'cmdline':
                tool = CommandLineTool()
            else:
                raise Exception, 'Unsupported tool type'
            
        #   Edit global fields
        tool.label = data['tool_name']
        tool.version = data['tool_version']
        tool.maintainer =  EDSAUser.objects.get(username='price')         #   TODO: FIX HACK
            
        #   Populate additional fields based on type of tool
        if data['tool_type'] == 'python':
            tool.module = data['rpm']
            
        elif data['tool_type'] == 'cmdline':
            tool.client_cmd = data['commands']

        #   Save result
        tool.save()
        
        #   Add ManyToMany info
        tool.machines.clear()
        for machine in data['machines']:
            tool.machines.add(machine)
        
        return tool
        
        
class CommandLineArgumentsForm(forms.Form):
    def __init__(self, tool, *args, **kwargs):
        super(CommandLineArgumentsForm, self).__init__(*args, **kwargs)
        
        self._inputs = tool.inputs.all().order_by('label')
        num_inputs = tool.inputs.all().count()
        pos_choices = range(1, num_inputs + 1)
        field_choices = zip(pos_choices, pos_choices)
        field_choices.append(('', 'Do not include'))
        
        for var in self._inputs:
            self.fields['position_' + var.label] = forms.ChoiceField(choices=field_choices)

    def get_field_pairs(self):
        return [(self.fields['position_' + var.label], var.label) for var in self._inputs]


""" Forms that manipulate Tasks """
    
class StartDependencyForm(forms.Form):
    """ Allow the user to choose a task to add dependencies to. """
    task = forms.ModelChoiceField(queryset=Task.objects.all(), widget=forms.HiddenInput)

class AddDependencyForm(ToolOrTaskForm):
    """ Collect information on dependencies for stitching together workflows. """
    
    def __init__(self, *args, **kwargs):
        #   Prevent conflicts based on field name 'tool' which may coexist on same page
        if 'prefix' not in kwargs:
            kwargs['prefix'] = 'dependency'
        super(AddDependencyForm, self).__init__(*args, **kwargs)
        self.show_fields(['task', 'tool'])
    
    existing_task = forms.ModelChoiceField(queryset=Task.objects.all(), widget=forms.HiddenInput)
    history = forms.ModelMultipleChoiceField(queryset=Task.objects.all(), widget=forms.HiddenInput, required=False)
    
    def clean(self):
        #   Check for cycles in the dependency graph that would be created if this change were applied.
        dep_task = self.cleaned_data.get('task')
        existing_task = self.cleaned_data.get('existing_task')
        history = self.cleaned_data.get('history')
        if dep_task == existing_task:
            raise forms.ValidationError('This would create a circular dependency.')
        if history:
            for hist_task in history:
                if dep_task == hist_task:
                    raise forms.ValidationError('This would create a circular dependency (cycle of length > 1).')
        return self.cleaned_data

class SelectStimulusTaskForm(AdjustableOnChangeForm):
    task = forms.ModelChoiceField(queryset=StimulusTask.objects.all(), widget=forms.Select(attrs={'dojoType': "dijit.form.Select", 'onChange': "update_form('/workflow/', 'select_stimulus_form', {default: 'pane_left'}, 'select_tool');"}))

class SelectTaskForm(AdjustableOnChangeForm):
    task = forms.ModelChoiceField(queryset=Task.objects.all(), widget=forms.Select(attrs={'dojoType': "dijit.form.Select", 'onChange': "update_form('/workflow/', 'select_task_form', {default: 'pane_left'}, 'workflow_select_task');"}))

class InvokerForm(SnatchArgumentsForm, HideableFieldsForm):
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    tool = forms.ModelChoiceField(queryset=Tool.objects.all())
    module = forms.ModelChoiceField(queryset=RegisteredPythonModule.objects.all())
    destination = forms.ChoiceField(choices=())
    line_number = forms.IntegerField(initial=1)
    seq = forms.IntegerField(initial=0)
    variables = forms.ModelMultipleChoiceField(queryset=Variable.objects.all())
    params = forms.CharField(max_length=1000, widget=JsonInputs)
    processor_type = forms.CharField(max_length=100)
        
    snatch_kwargs = ['tool', 'vp', 'direction']
    processor_type_map = {'inv': 'invoker', 'cap': 'capturer'}
        
    def __init__(self, *args, **kwargs):

        super(InvokerForm, self).__init__(*args, **kwargs)

        self.hide_fields(['tool', 'line_number', 'seq', 'processor_type'])

        if self._direction:
            self.dir_label = InvokerForm.processor_type_map[self._direction]
            self.fields['processor_type'].initial = self.dir_label
        if self._vp:
            self.load(self._vp)
            self._tool = self._vp.tool
            self.dir_label = self._vp.processor_type
            self.fields['processor_type'].initial = self.dir_label
        if self._tool:
            self.fields['tool'].initial = self._tool
            existing_vp = self._tool.variableprocessor_set.filter(processor_type=self.dir_label).order_by('-seq')
            if existing_vp.exists() and self.fields['seq'].initial is None:
                self.fields['seq'].initial = existing_vp[0].seq + 10
                
        if not hasattr(self, 'dir_label') and self.data:
            self.dir_label = self.data['processor_type']
        if self.dir_label == 'invoker':
            self.fields['destination'].choices = (('stdin', 'Standard input'), ('file', 'File'), ('arguments', 'Command-line arguments'))
        elif self.dir_label == 'capturer':
            self.fields['destination'].choices = (('stdout', 'Standard output'), ('stderr', 'Standard error'), ('file', 'File'))

    def load(self, vp):
        self.fields['id'].initial = vp.id
        self.fields['tool'].initial = vp.tool
        self.fields['seq'].initial = vp.seq
        self.fields['module'].initial = vp.module
        self.fields['line_number'].initial = vp.line_number
        self.fields['destination'].initial = vp.context
        self.fields['variables'].initial = vp.variables.all()
        self.fields['params'].initial = vp._params
        self.fields['processor_type'].initial = vp.processor_type
    
    def save(self):
        if 'id' not in self.cleaned_data or not self.cleaned_data['id']:
            vp = VariableProcessor()
        else:
            vp = VariableProcessor.objects.get(id=self.cleaned_data['id'])
            
        vp.processor_type = self.cleaned_data['processor_type']
        vp.context = self.cleaned_data['destination']
        vp.tool = get_subclass_instance(self.cleaned_data['tool'])
        vp.module = self.cleaned_data['module']
        vp.seq = self.cleaned_data['seq']
        vp._params = self.cleaned_data['params']
        vp.line_number = self.cleaned_data['line_number']
        vp.save()
        
        vp.variables.clear()
        for var in self.cleaned_data['variables']:
            vp.variables.add(var)

        return vp
        
