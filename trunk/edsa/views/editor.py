
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
""" Views for editing tools. """

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django import forms

from edsa.clients.forms import ToolConfigForm, RegisteredPythonModuleForm, VariableSetForm
from edsa.clients.forms import SelectToolForm, CreateToolForm, RunToolForm, InvokerForm
from edsa.data.forms import VariableForm, UnitForm

from edsa.log.models import Log
from edsa.data.models import DataValue, Variable, BaseUnit, Unit, VarType
from edsa.clients.models import Task, Tool, StimulusTask, RegisteredPythonModule, VariableProcessor, CommandLineTool

from edsa.utils.subclass import get_subclass_instance
from edsa.utils.ajax import AjaxHandler
from edsa.utils.rendering import render_to_response, render_to_json

import simplejson as json
import pylab


class EditorHandler(AjaxHandler):
    FORM_MAPPING = {
        'rpm_form': RegisteredPythonModuleForm,
        'config_form': ToolConfigForm,
        'select_tool_form': SelectToolForm,
        'create_tool_form': CreateToolForm,
        'var_in_form': VariableSetForm,
        'var_out_form': VariableSetForm,
        'variable_in_form': VariableForm,
        'variable_out_form': VariableForm,
        'unit_in_form': UnitForm,
        'unit_out_form': UnitForm,
        'vp_form': InvokerForm,
    }

    def add_rpm(self):
        """ Display a form for adding a new RegisteredPythonModule. """
        self.temp_context['rpm_form'] = RegisteredPythonModuleForm()
        response_context = {}
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/add_rpm.html', self.temp_context)
        return response_context
        
    def save_rpm(self):
        """ Save a RegisteredPythonModule from a form. """
        response_context = {}
        rpm_form = self.form_dict['rpm_form']
        if rpm_form.is_valid():
            #   Save RPM
            result = rpm_form.save()
            result.save()
            print 'Saved form to %s' % result
            #   Update tool config form to use new module
            self.form_dict['config_form'].data['rpm'] = result.id
            print 'Making ToolConfigForm: %s' % self.form_dict['config_form']
            config_form = self.form_dict['config_form']
            config_form.fields['rpm'].data = result
            self.temp_context['config_form'] = config_form
            response_context['%s_html' % self.targets['config']] = render_to_string('ajax_fragments/tool_config_base.html', self.temp_context)
        else:
            #   Display form again
            self.temp_context['rpm_form'] = rpm_form
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/add_rpm.html', self.temp_context)
        return response_context

    def set_tool_type(self):
        """ Display the appropriate configuration form based on whether
            a PythonTool or CommandLineTool is desired
        """
        config_form = self.form_dict['config_form']
        self.temp_context['config_form'] = config_form
        response_context = {}
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/tool_config_base.html', self.temp_context)
        return response_context

    def add_vp_info(self, tool):
        result = []
        if isinstance(tool, CommandLineTool):
            result.append({'name': 'invokers', 'label': 'Invokers', 'shortname': 'inv', 'vps': tool.invokers})
            result.append({'name': 'capturers', 'label': 'Capturers', 'shortname': 'cap', 'vps': tool.capturers})
        self.temp_context['variableprocessors'] = result
        print self.temp_context['variableprocessors']

    def init_tool(self):
        """ Start the process of editing a new Tool, but don't save it
            to the database yet (required fields still need to be filled in)
        """
        create_form = self.form_dict['create_tool_form']
        config_form = ToolConfigForm(initial=create_form.data)
        self.temp_context['config_form'] = config_form
        #   Compensate for different field names between the two forms
        self.temp_context['config_form'].initial['tool_version'] = self.temp_context['config_form'].initial['version']
        response_context = {}
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/tool_config_base.html', self.temp_context)
        return response_context

    def select_tool(self):
        """ Choose an existing tool to modify """
        response_context = {}
        select_form = self.form_dict['select_tool_form']
        if select_form.is_valid():
            #   Generate a form for the specified tool
            tool = select_form.cleaned_data['tool']
            config_form = ToolConfigForm()
            config_form.load(tool)
            self.temp_context['config_form'] = config_form
            tool = get_subclass_instance(tool)
            self.add_vp_info(tool)
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/tool_config_base.html', self.temp_context)
            
            #   Render tabs for input and output variables of this tool
            self.temp_context['var_in_form'] = VariableSetForm(tool=tool, dir='in')
            self.temp_context['var_out_form'] = VariableSetForm(tool=tool, dir='out')
            response_context['%s_html' % self.targets['vars_in']] = render_to_string('ajax_fragments/var_in_config.html', self.temp_context)
            response_context['%s_html' % self.targets['vars_out']] = render_to_string('ajax_fragments/var_out_config.html', self.temp_context)     

            #   Render log table
            if 'log' in self.targets:
                self.temp_context['log'] = tool.get_log_table()
                response_context['%s_html' % self.targets['log']] = render_to_string('ajax_fragments/tool_log_table.html', self.temp_context) 
        return response_context
        
    def configure_tool(self):
        """ Save basic configuration, creating a new tool and allowing the
            variables to be edited
        """
        response_context = {}
        config_form = self.form_dict['config_form']
        tool = None
        if config_form.is_valid(): 
            tool = config_form.save()
            self.temp_context['var_in_form'] = VariableSetForm(tool=tool, dir='in')
            self.temp_context['var_out_form'] = VariableSetForm(tool=tool, dir='out')
            if 'vars_in' in self.targets:
                response_context['%s_html' % self.targets['vars_in']] = render_to_string('ajax_fragments/var_in_config.html', self.temp_context)
            if 'vars_out' in self.targets:
                response_context['%s_html' % self.targets['vars_out']] = render_to_string('ajax_fragments/var_out_config.html', self.temp_context)
        if tool:
            self.add_vp_info(tool)
        self.temp_context['config_form'] = config_form
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/tool_config_base.html', self.temp_context)
        return response_context
        
    def update_in_vars(self):
        """ Let the VariableSetForm for the input variables rewrite itself 
            based on a change 
        """
        response_context = {}
        var_form = self.form_dict['var_in_form']
        self.temp_context['var_in_form'] = var_form
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/var_in_config.html', self.temp_context)
        return response_context

    def update_out_vars(self):
        """ Let the VariableSetForm for the output variables rewrite itself 
            based on a change 
        """
        response_context = {}
        var_form = self.form_dict['var_out_form']
        self.temp_context['var_out_form'] = var_form
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/var_out_config.html', self.temp_context)
        return response_context

    def add_variable(self):
        """ Display a new tab in which a new variable can be created """
        response_context = {}
        var_form = VariableForm()
        #   Infer direction of variable to be added
        if 'var_in' in self.default_target:
            self.temp_context['direction'] = 'in'
            self.temp_context['tab'] = 'center'
        elif 'var_out' in self.default_target:
            self.temp_context['direction'] = 'out'
            self.temp_context['tab'] = 'right'
        #   Draw new form
        self.temp_context['var_form'] = var_form
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/variable_form.html', self.temp_context)
        return response_context
            
    def save_variable(self):
        """ Save a new variable from the 'Add Variable' tab """
        response_context = {}
        
        #   Infer direction of the new variable for the current tool
        if 'variable_in_form' in self.form_dict:
            direction = 'in'
            tab = 'center'
        else:
            direction = 'out'
            tab = 'right'
        self.temp_context['direction'] = direction
        self.temp_context['tab'] = tab
        
        #   Validate form
        variable_form = self.form_dict['variable_%s_form' % direction]
        if variable_form.is_valid():
            #   Rely on form class to save new variable
            result = variable_form.save()
            var_new_form = self.form_dict['var_%s_form' % direction]
            var_new_form.add_variable(result)
            self.temp_context['var_%s_form' % direction] = var_new_form
            response_context['%s_html' % self.targets['%sputs' % direction]] = render_to_string('ajax_fragments/var_%s_config.html' % direction, self.temp_context)
        else:
            self.temp_context['var_form'] = variable_form
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/variable_form.html', self.temp_context)
        return response_context
                
    def add_unit(self):
        """ Display a new tab in which a new unit can be created for the
            variable that is currently being edited
        """
        response_context = {}
        
        #   Infer direction of the current variable for the current tool
        if 'variable_in_form' in self.form_dict:
            direction = 'in'
            tab = 'center'
        else:
            direction = 'out'
            tab = 'right'
        
        #   Display form for new unit
        self.temp_context['unit_form'] = UnitForm()
        self.temp_context['direction'] = direction
        self.temp_context['tab'] = tab
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/unit_form.html', self.temp_context)
        return response_context
 
    def save_unit(self):
        """ Save a new unit from the 'Add Unit' tab """
        response_context = {}
        
        #   Infer direction of the current variable for the current tool
        if 'unit_in_form' in self.form_dict:
            direction = 'in'
            tab = 'center'
        else:
            direction = 'out'
            tab = 'right'
        self.temp_context['direction'] = direction
        self.temp_context['tab'] = tab
        
        #   Validate form
        unit_form = self.form_dict['unit_%s_form' % direction]
        if unit_form.is_valid():
            result = unit_form.save()
            variable_form = self.form_dict['variable_%s_form' % direction]
            #   Rewrite the unit field and unbind form
            variable_form.fields['unit'] = forms.ModelChoiceField(queryset=BaseUnit.objects.all(), widget=forms.Select(attrs={'dojoType':"dijit.form.Select", 'value': result.id}), initial=result)
            variable_form.initial = variable_form.data
            variable_form.is_bound = False
            self.temp_context['var_form'] = variable_form
            response_context['%s_html' % self.targets['variable']] = render_to_string('ajax_fragments/variable_form.html', self.temp_context)
        else:
            self.temp_context['unit_form'] = unit_form
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/unit_form.html', self.temp_context)
        return response_context
        
    def get_vp(self, begin_str):
        form_label = None
        all_forms = self.form_data_dict.keys()
        for form in all_forms:
            if form.startswith(begin_str):
                form_label = form
                break
        if form_label:
            vp_id = self.form_data_dict[form_label]['vp_id']
            return VariableProcessor.objects.get(id=vp_id)
        else:
            return None
            
    def vp_handler_base(self, processor_type, direction=None):
        vp = self.get_vp('%s_select_form' % processor_type)
        if processor_type == 'inv':
            other_vps = vp.tool.invokers
        elif processor_type == 'cap':
            other_vps = vp.tool.capturers
        my_index = list(other_vps).index(vp)\
        
        if direction:
            other_vp = None
            if direction == 'up':
                selected_vp = other_vps[my_index]
                if my_index > 0:
                    other_vp = other_vps[my_index - 1]
            elif direction == 'down':
                selected_vp = other_vps[my_index]
                if my_index < len(other_vps) - 1:
                    other_vp = other_vps[my_index + 1]
            if other_vp:
                temp_seq = other_vp.seq
                other_vp.seq = selected_vp.seq
                selected_vp.seq = temp_seq
                selected_vp.save()
                other_vp.save()
            
        return self.configure_tool()
        
    def move_invokers_up(self):
        return self.vp_handler_base('inv', 'up')
    def move_invokers_down(self):
        return self.vp_handler_base('inv', 'down')
    def move_capturers_up(self):
        return self.vp_handler_base('cap', 'up')
    def move_capturers_down(self):
        return self.vp_handler_base('cap', 'down')

    def edit_vp(self, direction=None):
        response_context = {}
        vp = self.get_vp('inv_select_form')
        if not vp:
            vp = self.get_vp('cap_select_form')
        
        if not vp:
            #   New VP requested.
            form = InvokerForm(tool=CommandLineTool.objects.get(id=self.form_data_dict['config_form']['existing_tool']), direction=direction)
        else:
            form = InvokerForm(vp=vp)
        self.temp_context['vp_form'] = form
        self.temp_context['vp'] = vp
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/edit_vp.html', self.temp_context)
        
        return response_context
    
    def edit_invokers(self):
        return self.edit_vp('inv')
    def edit_capturers(self):
        return self.edit_vp('cap')

    def save_vp(self):
        response_context = {}
        
        form = self.form_dict['vp_form']
        
        if form.is_valid():
            vp = form.save()
            print 'Saved %s' % vp
            other_context = self.configure_tool()
            response_context['%s_html' % self.targets['tool_config']] = other_context['%s_html' % self.default_target]
        else:
            vp_id = form.data['id']
            if vp_id:
                vp = VariableProcessor.objects.get(id=vp_id)
            else:
                vp = None
            self.temp_context['vp_form'] = form
            self.temp_context['vp'] = vp
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/edit_vp.html', self.temp_context)

        return response_context
    
    def delete_vp(self):
        response_context = {}
        vp = self.get_vp('inv_select_form')
        if not vp:
            vp = self.get_vp('cap_select_form')
        vp.delete()
        return self.configure_tool()
    delete_capturers = delete_vp
    delete_invokers = delete_vp

@login_required
def tool_editor(request, extra=''):

    if extra == 'ajax_update':
        #   Handle based on type of request
        handler = EditorHandler()
        response_context = handler.handle(request, extra)
        return render_to_json(response_context)

    else:
        #   Display main tool editor page
        form = CreateToolForm()
        select_form = SelectToolForm()

        context = {}
        context['create_form'] = form
        context['select_form'] = select_form
 
        return render_to_response('EditJS.html', context, request)