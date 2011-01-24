
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
""" Views for arranging tasks into workflows. """

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django import forms

from edsa.clients.forms import SelectToolForm, SelectStimulusTaskForm, SelectTaskForm, AddDependencyForm, StartDependencyForm

from edsa.clients.models import Task, Tool, StimulusTask, RegisteredPythonModule

from edsa.utils.subclass import get_subclass_instance
from edsa.utils.ajax import AjaxHandler
from edsa.utils.rendering import render_to_response, render_to_json

import simplejson as json


class WorkflowHandler(AjaxHandler):
    FORM_MAPPING = {
        'create_task_form': SelectToolForm,
        'select_task_form': SelectTaskForm,
        'start_dep_form': StartDependencyForm,
        'add_dep_form': AddDependencyForm,
    }
    
    def init_task(self):
        """ Create a new Task with no dependencies from an existing Tool. """
        response_context = {}
        form = self.form_dict['create_task_form']
        if form.is_valid():
            #   Wrap tool into a task
            self.temp_context['tool'] = form.cleaned_data['tool']
            new_task = Task()
            new_task.tool = form.cleaned_data['tool']
            new_task.save()
            self.temp_context['task'] = new_task
            
            #   Update select form with the new task
            self.temp_context['select_form'] = SelectTaskForm(initial={'task': new_task})
            response_context['pane_edit_task_html'] = render_to_string('ajax_fragments/workflow_select_task.html', self.temp_context)
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/configure_task.html', self.temp_context)
            
        return response_context

    def workflow_select_task(self):
        """ Show options for modifying the selected Task. """
        response_context = {}
        form = self.form_dict['select_task_form']
        if form.is_valid():
            self.temp_context['task'] = form.cleaned_data['task']
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/configure_task.html', self.temp_context)
        return response_context
        
    def add_dependency(self):
        """ Show a new tab which lets you choose a Tool or Task to be added as a dependency
            of the Task that is currently being edited. 
        """
        response_context = {}
        #   Search for active 'start_dep' form (there may be more than 1)
        form = None
        for key in self.form_dict:
            if key.startswith('start_dep'):
                form = self.form_dict[key]
        print form.data
        if form and form.is_valid():
            task = form.cleaned_data['task']
            #   History is the sequence of all task IDs leading to the root of this dependency tree.
            #   If you have this information, fetch it for use by the form in the new tab.
            if 'history' in form.data:
                history = form.data['history'].split(",")
            else:
                history = []
            self.temp_context['task'] = task
            self.temp_context['add_form'] = AddDependencyForm(initial={'existing_task': task, 'history': Task.objects.filter(id__in=history)})
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/add_dependency.html', self.temp_context)
        return response_context
        
    def save_dependency(self):
        """ Link the specified task or tool into the current dependency chain. """
        
        response_context = {}
        #   The add_dep_form has a prefix, typically 'dependency' to avoid DOM ID conflicts.
        form = self.form_dict['add_dep_form']
        prefix = form.prefix
        form.data[prefix+'-history'] = json.loads(form.data[prefix+'-history'].replace("'", '"'))
        print form.data
        if form.is_valid():
            #   Save the dependency
            task = form.cleaned_data['existing_task']
            if form.cleaned_data['tool']:
                #   If a tool was specified, wrap the tool in a new task 
                print 'Adding task for tool %s' % form.cleaned_data['tool']
                new_task = Task()
                new_task.tool = form.cleaned_data['tool']
                new_task.save()
                task.dependencies.add(new_task)
            elif form.cleaned_data['task']:
                #   If a task was specified, simply link it up
                task.dependencies.add(form.cleaned_data['task'])
            else:
                raise Exception, 'Form provided no new dependency.'
            #   Update the form on the original tab
            self.default_target = self.targets['config']
            return self.workflow_select_task()
        else:
            #   If there was an error in the form, return it to the form tab
            self.temp_context['task'] = form.data[prefix+'-existing_task']
            self.temp_context['add_form'] = form
            response_context['%s_html' % self.default_target] = render_to_string('ajax_fragments/add_dependency.html', self.temp_context)
            return response_context

    def remove_dependency(self):
        """ Unlink the specified task from the current dependency chain. """
        #   Search for active 'start_dep' form (there may be more than 1)
        form = None
        for key in self.form_dict:
            if key.startswith('start_dep'):
                form = self.form_dict[key]
        if form and form.is_valid():\
            #   Unlink task
            task = form.cleaned_data['task']
            parent = Task.objects.get(id=form.data['parent'])
            parent.dependencies.remove(task)
        #   Redisplay form
        self.form_dict['select_task_form'] = SelectTaskForm({'task': form.data['root']})
        return self.workflow_select_task()


def workflow_editor(request, extra=''):
    if extra == 'ajax_update':
        handler = WorkflowHandler()
        response_context = handler.handle(request, extra)
        return render_to_json(response_context)
    else:
        #   Display main workflow editor page
        context = {}
        context['select_form'] = SelectTaskForm()
        context['start_form'] = SelectToolForm(onchange_tool='dijit.byId(\'submit_create_form\').attr(\'disabled\', false);')
        return render_to_response('workflow_editor.html', context)
