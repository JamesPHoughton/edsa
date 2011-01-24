
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
""" Views for launching tools and tasks. """

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django import forms

from edsa.clients.forms import SelectToolForm, SelectStimulusTaskForm, SelectTaskForm, RunToolForm
from edsa.data.forms import VariableForm, UnitForm, EditValueForm, SelectValueForm

from edsa.log.models import Log
from edsa.data.models import DataValue, Variable, VarType
from edsa.clients.models import Task, Tool, StimulusTask, Machine
from edsa.tags.models import DataCategory
from edsa.utils.subclass import get_subclass_instance
from edsa.utils.ajax import AjaxHandler
from edsa.utils.rendering import render_to_response, render_to_json

import simplejson as json


class LauncherHandler(AjaxHandler):
    FORM_MAPPING = {
        'select_tool_form': SelectToolForm,
        'select_task_form': SelectTaskForm,
        'select_stimulus_form': SelectStimulusTaskForm,
        'multiple_tool_form': SelectStimulusTaskForm,
        'single_tool_form': RunToolForm,
        'select_value_form': SelectValueForm,
        'edit_value_form': EditValueForm,
    }
    
    def select_value(self):
        """ Display a form allowing the user to choose from recent values. """
        response_context = {}
        
        #   Try to guess the ID of the variable we want to edit.
        var_id = None
        form_id = None
        for key in self.form_data_dict:
            if key.startswith('var_summary_'):
                form_id = key
                var_id = int(key[len('var_summary_'):])
                break
                
        if var_id:
            #   If a variable was selected, create a form with its values.
            var = Variable.objects.get(id=var_id)
            initial_data = {}
            if 'tool' in self.form_data_dict[form_id]:
                initial_data['tool'] = self.form_data_dict[form_id]['tool']
            if 'task' in self.form_data_dict[form_id]:
                initial_data['task'] = self.form_data_dict[form_id]['task']
            form = SelectValueForm(variable=var, initial=initial_data)
            self.temp_context['variable'] = var
            self.temp_context['value_form'] = form
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/select_value.html', self.temp_context)
            
        return response_context
        
    def edit_value(self):
        """ Display a form allowing the user to enter in a new value for a variable. """
        response_context = {}
        
        #   Try to guess the ID of the variable we want to edit.
        var_id = None
        form_id = None
        for key in self.form_data_dict:
            if key.startswith('var_summary_'):
                form_id = key
                var_id = int(key[len('var_summary_'):])
                break
                
        if var_id:
            #   If a variable was selected, create a form that allows new values to be added.
            var = Variable.objects.get(id=var_id)
            initial_data = {}
            if 'tool' in self.form_data_dict[form_id]:
                initial_data['tool'] = self.form_data_dict[form_id]['tool']
            if 'task' in self.form_data_dict[form_id]:
                initial_data['task'] = self.form_data_dict[form_id]['task']
            form = EditValueForm(variable=var, initial=initial_data)
            self.temp_context['variable'] = var
            self.temp_context['value_form'] = form
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/edit_value.html', self.temp_context)
            
        return response_context
        
    def save_value(self):
        """ Save a new value from the form displayed by either select_value()
            or edit_value().
        """
        response_context = {}
        
        form = None
        
        if 'select_value_form' in self.form_dict:
            form = self.form_dict['select_value_form']
            if form.is_valid():
                value = form.cleaned_data['value']
                variable = form.cleaned_data['variable']
                #   For now, set the latest value to a copy of the selected one
                new_value = value
                new_value.id = None
                new_value.save()
            else:
                self.temp_context['variable'] = form.fields['variable'].initial
                self.temp_context['value_form'] = form
                response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/select_value.html', self.temp_context)
        elif 'edit_value_form' in self.form_dict:
            form = self.form_dict['edit_value_form']
            print 'Got form %s with value field %s' % (type(form), type(form.fields['value']))
            if form.is_valid():
                #   Because the 'value' FormField is customized based on the 
                #   variable's VarType, cleaned_data['value'] is already the
                #   proper Python type to be saved.
                value_contents = form.cleaned_data['value']
                variable = form.cleaned_data['variable']
                new_value = DataValue()
                new_value.data = value_contents
                #   Populate other fields
                new_value.category = form.cleaned_data['category']
                new_value.variable = variable
                new_value.save()
            else:
                self.temp_context['variable'] = form.fields['variable'].initial
                self.temp_context['value_form'] = form
                response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/edit_value.html', self.temp_context)
        else:
            raise Exception, 'No form submitted'
        
        #   Use helper functions to redisplay left panel, but redirect output to correct tab
        
        if form and form.is_valid():
            tool = form.cleaned_data.get('tool')
            if tool:
                new_context = self.launcher_output_tool(tool)
                response_context['%s_html' % self.targets['vars_in']] = new_context['%s_html' % self.targets['vars_in']]
                #   response_context['%s_html' % self.targets['config']] = new_context['%s_html' % self.default_target]
            task = form.cleaned_data.get('task')
            if task:
                new_context = self.launcher_output_task(task)
                response_context['%s_html' % self.targets['vars_in']] = new_context['%s_html' % self.targets['vars_in']]
                #   response_context['%s_html' % self.targets['config']] = new_context['%s_html' % self.default_target]

        return response_context
    
    """ Helper functions for launcher_select_tool and others """
    def launcher_output_task(self, task, response_context={}):
        """ Generate output for the launcher panel when a task has been selected """
        
        #   Fetch available instances of all tools needed for this task
        self.temp_context['task'] = task
        self.temp_context['tools'] = [x.tool for x in task.all_dependencies()] + [task.tool]
        machine_available = True
        machines_available = Tool.get_available(self.temp_context['tools'])
        machine_instances = []
        for item in self.temp_context['tools']:
            if item.id in machines_available:
                machine_instances.append([y['machine_name'] for y in machines_available[item.id].instances])
            else:
                machine_instances.append([])
                
        #   Prepare tool config forms
        self.temp_context['tool_forms'] = []
        for i in range(len(self.temp_context['tools'])):
            tool = self.temp_context['tools'][i]

            #   Check availability of machine for this tool
            if len(machine_instances[i]) == 0:
                machine_available = False
                continue
            machine_id = Machine.objects.get(label=machine_instances[i][0]).id
            tool_form = RunToolForm(tool=tool, machines=machine_instances[i], initial={'machine': machine_id, 'seq': i}, prefix='tool_%d_%d' % (tool.id, i))
            tool_form.machines = machine_instances[i]
            self.temp_context['tool_forms'].append(tool_form)
        self.temp_context['machine_available'] = machine_available
        self.temp_context['variables'] = task.inputs()
                
        #   Render output for run control
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/task_run.html', self.temp_context)
        response_context['%s_html' % self.targets['vars_in']] = render_to_string('ajax_fragments/task_vars_summary.html', self.temp_context)
        return response_context

    def launcher_output_tool(self, tool, response_context={}):
        """ Generate output for the launcher panel when a tool has been selected """
        
        #   Fetch available instances (machine bindings) of the tool
        self.temp_context['tool'] = tool
        machine_instances = Tool.get_available(tool)
        if tool.id in machine_instances:
            machine_available = True
            self.temp_context['machines'] = [x['machine_name'] for x in machine_instances[tool.id].instances]
            machine_id = Machine.objects.get(label=self.temp_context['machines'][0]).id
            self.temp_context['tool_form'] = RunToolForm(tool=tool, initial={'machine': machine_id}, machines=self.temp_context['machines'], prefix='tool_%d' % tool.id)
        else:
            machine_available = False
            self.temp_context['machines'] = []

        #   Gather input variables
        self.temp_context['variables'] = tool.inputs.all()
        self.temp_context['machine_available'] = machine_available

        #   Render output, optionally including log table
        response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/task_run.html', self.temp_context)
        response_context['%s_html' % self.targets['vars_in']] = render_to_string('ajax_fragments/task_vars_summary.html', self.temp_context)
        if 'log' in self.targets:
            self.temp_context['log'] = tool.get_log_table()
            response_context['%s_html' % self.targets['log']] = render_to_string('ajax_fragments/tool_log_table.html', self.temp_context) 
        
        return response_context
    
    def launcher_select_tool(self):
        """ Select a tool or task to run """
        
        response_context = {}
        machine_available = None
        if 'select_tool_form' in self.form_dict:
            select_form = self.form_dict['select_tool_form']
            using_tool = True
        elif 'select_task_form' in self.form_dict:
            select_form = self.form_dict['select_task_form']
            using_tool = False
        elif 'select_stimulus_form' in self.form_dict:
            #   Stimulus task not yet supported properly in the run_tool view below
            select_form  = self.form_dict['select_stimulus_form']
            using_tool = False
        else:
            raise Exception, 'No appropriate form found for select_tool'
            
        if 'select_stimulus_form' in self.form_dict:
            select_form.prefix = 'stimulus'
        if select_form.is_valid():
            #   Call the helper function launcher_output_{tool, task} to generate output
            self.temp_context['multiple_tools'] = not using_tool
            if using_tool:
                tool = select_form.cleaned_data['tool']
                return self.launcher_output_tool(tool)
            else:
                task = select_form.cleaned_data['task']
                return self.launcher_output_task(task)

        return response_context

    def run_tool(self):
        """ Execute a single tool """
        
        response_context = {}
        print 'Running tool'
        if 'single_tool_form' in self.form_dict:

            #   Override form creation since the prefix has been adjusted
            tool_id = self.form_data_dict['single_tool_form']['tool_id']
            form_prefix = 'tool_%s' % tool_id
            form = RunToolForm(self.form_data_dict['single_tool_form'], prefix=form_prefix)
            if form.is_valid():
                tool = form.cleaned_data['tool']
                
                #   Optionally load parameters (if the user entered them correctly)
                try:
                    params = json.loads(form.cleaned_data['params'])
                except:
                    params = {}
                machine = form.cleaned_data['machine']
                
                #   Execute the tool on the remote machine
                proxy = tool.get_proxy(machine.label)
                if not proxy:
                    print 'Error - machine %s disappeared.' % machine
                else:
                    input_vals = [var.latest_value() for var in tool.inputs.all()]
                    print 'Input values: %s' % input_vals
                    vals_ok = True
                    for val in input_vals:
                        if val is None:
                            vals_ok = False
                            self.temp_context['result'] = 'Please ensure that all variables are bound to values.'
                    if vals_ok:
                        self.temp_context['result'] = proxy.run(input_vals, params)
                    self.temp_context['variables'] = tool.outputs.all()
                    
                #   Render results
                self.temp_context['using_tool'] = True
                response_context['%s_html' % self.targets['results']] = render_to_string('ajax_fragments/task_run_result.html', self.temp_context)
                if 'log' in self.targets:
                    self.temp_context['log'] = tool.get_log_table()
                    response_context['%s_html' % self.targets['log']] = render_to_string('ajax_fragments/tool_log_table.html', self.temp_context) 
                
            else:
                print 'Encountered problem in form'
                self.temp_context['machine_available'] = True
                self.temp_context['using_tool'] = True
                self.temp_context['tool_form'] = form
                response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/task_run.html', self.temp_context)

        return response_context
    
    def run_task(self):
        """ Execute one or more tools in a dependency tree """
        response_context = {}
        
        if 'multiple_tool_form' in self.form_dict:
            #   Override form creation since the prefixes have been customized
            #   per tool, per instance.  (A given tool may need to be run more
            #   than once, and we want to keep track of the specified machine
            #   and parameters for each run separately.)
            ignore_keys = ['task_id', 'form_prefix']
            task_id = int(self.form_data_dict['multiple_tool_form']['task_id'])
            task = Task.objects.get(id=task_id)
            failure = False
            all_keys = self.form_data_dict['multiple_tool_form'].keys()
            prefixes_so_far = []
            tool_keys = []
            form_data = self.form_data_dict['multiple_tool_form']
            for key in all_keys:
                form_prefix = key.split('-')[0]
                if form_prefix not in ignore_keys and form_prefix not in prefixes_so_far:
                    tool_id = int(form_prefix.split('_')[1])
                    seq = int(form_data[form_prefix+'-seq'])
                    print 'Got prefix: %s (seq: %s)' % (form_prefix, seq)
                    prefixes_so_far.append(form_prefix)
                    tool_keys.append((seq, tool_id, form_prefix))

            #   Step through tool instances in proper order
            tool_keys.sort(key=lambda x: x[0])
            self.temp_context['results'] = []
            self.temp_context['task'] = task
            for key in tool_keys:
                form = RunToolForm(form_data, prefix=key[2])
                if form.is_valid():
                    #   Run the tool on the remote machine
                    #   TODO: Support running StimulusTask using its features
                    tool = form.cleaned_data['tool']
                    input_vals = [var.latest_value() for var in tool.inputs.all()]
                    params = json.loads(form.cleaned_data['params'])
                    machine = form.cleaned_data['machine']
                    result = tool.get_proxy(machine.label).run(input_vals, params)
                    print 'Ran %s on %s with result %s' % (tool, form.cleaned_data['machine'].label, result)
                    self.temp_context['results'].append({'tool': tool, 'result': result})
                else:
                    #   TODO: Accumulate all forms so they're editing the form they started with
                    failure = True
                    print 'Encountered problem in form'
                    self.temp_context['machine_available'] = True
                    self.temp_context['using_tool'] = False

            #   Render output
            if failure:
                response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/task_run.html', self.temp_context)
            else:
                self.temp_context['variables'] = self.temp_context['variables'] = task.outputs()
                response_context['%s_html' % self.targets['results']] = render_to_string('ajax_fragments/task_run_result.html', self.temp_context)

        return response_context

@login_required   
def tool_launcher(request, extra=''):

    if extra == 'ajax_update':
        #   Handle based on type of request
        handler = LauncherHandler()
        response_context = handler.handle(request, extra)
        return render_to_json(response_context)

    else:
        #   Display main tool launcher page
        form1 = SelectToolForm(onchange_tool='update_form(\'/setup/\', \'select_tool_form\', {default: \'pane_configure\', vars_in: \'pane_inputs\', log: \'footer\'}, \'launcher_select_tool\');')
        form2 = SelectTaskForm(onchange_task='update_form(\'/setup/\', \'select_task_form\', {default: \'pane_configure\', vars_in: \'pane_inputs\', log: \'footer\'}, \'launcher_select_tool\');')
        form3 = SelectStimulusTaskForm(prefix='stimulus', onchange_task='update_form(\'/setup/\', \'select_stimulus_form\', {default: \'pane_configure\', vars_in: \'pane_inputs\', log: \'footer\'}, \'launcher_select_tool\');')
        context = {}
        context['select_tool_form'] = form1
        context['select_task_form'] = form2
        context['select_stimulus_form'] = form3
        return render_to_response('RunTool.html', context)
        