
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
""" EDSA Clients models
    - additional user info
    - permissions
    - projects
    - tools
    - clients
    - tasks
"""

from django.db import models
from django.contrib.auth.models import User
from edsa.utils.uris import get_machine_name, generate_uri, get_object_label, generate_object_label
from edsa.utils.subclass import get_subclass_instance

import simplejson as json
import random
from datetime import datetime

""" Snippet from http://www.djangosnippets.org/snippets/912/ """

class Country(models.Model):
    """Model for countries"""
    iso_code = models.CharField(max_length = 2, primary_key = True)
    name = models.CharField(max_length = 45, blank = False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name", "iso_code"]

class StateProvince(models.Model):
    """Model for states and provinces"""
    iso_code = models.CharField(max_length = 3, primary_key = True)
    name = models.CharField(max_length = 55, blank = False)
    country = models.ForeignKey(Country, to_field="iso_code")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "State or province"

class Address(models.Model):
    """Model to store addresses for accounts"""
    
    #   Added contactinfo foreign key to ensure that each address is tied to a contactinfo;
    #   added label for associating multiple addresses with a user
    #   Michael Price 3/1/2010
    contactinfo = models.ForeignKey('ContactInfo')
    label = models.CharField("Description", max_length=32)
    
    address_line1 = models.CharField("Address line 1", max_length = 45)
    address_line2 = models.CharField("Address line 2", max_length = 45,
        blank = True)
    postal_code = models.CharField("Postal Code", max_length = 10)
    city = models.CharField(max_length = 50, blank = False)
    state_province = models.ForeignKey(StateProvince)
    country = models.ForeignKey(Country, blank = False)

    def __unicode__(self):
        return u'%s: %s %s, %s, %s %s (%s)' % (self.label, self.address_line1, self.address_line2, self.city, self.state_province.iso_code, self.postal_code, self.country.iso_code)

    class Meta:
        verbose_name_plural = "Addresses"
        unique_together = ("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")

""" End of snippet """


class EDSAUser(User):
    """ A proxy model to provide additional functions using the relationships 
        defined below. """
    
    #   Access the biography using manager: biography
    #   Access the contact info using manager: contactinfo
    #   Access the institution using contact info.institution
        
    class Meta:
        proxy = True
        
    def _get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

class Biography(models.Model):
    """ A biographical description (including a picture) for a user. """
    
    user = models.OneToOneField(EDSAUser)
    summary = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='uploaded/bio_images', max_length=255)
    
    def __unicode__(self):
        return '%s: %s' % (self.user.username, self.summary)

class Institution(models.Model):
    """ Information about a company, university, or government agency. """
    
    name = models.CharField(max_length=80)
    description = models.TextField()
    url = models.URLField()
    
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.url)

class ContactInfo(models.Model):
    """ Contact information to be associated with a user 
        (i.e. where they work). 
    """
    
    user = models.OneToOneField(EDSAUser)
    department = models.CharField(max_length=80)
    institution = models.ForeignKey(Institution)
    last_updated = models.DateTimeField(auto_now=True)
    #   Access the addresses using manager: address_set 

    def __unicode__(self):
        return u'%s: %s of %s' % (self.user.username, self.department, self.institution.name)

class Machine(models.Model):
    """ Information about a machine on which the EDSA client is installed. """
    
    label = models.CharField(max_length=80)
    maintainer = models.ForeignKey(EDSAUser)
    ip_addr = models.IPAddressField()
    #   access tools with manager
    #   execute RPC call to get status, invoke tools
    
    def __unicode__(self):
        return u'%s (%s) - %s' % (self.label, self.ip_addr, self.maintainer)

class Tool(models.Model):
    """ Metadata for a software tool that can be installed on client machines. """
    
    label = models.CharField(max_length=80)
    version = models.CharField(max_length=20, blank=True, null=True)
    maintainer = models.ForeignKey(EDSAUser)
    
    inputs = models.ManyToManyField('data.Variable', related_name='tool_inputs')
    input_constraints = models.ManyToManyField('data.Constraint', related_name='tool_input_constraints', blank=True)

    outputs = models.ManyToManyField('data.Variable', related_name='tool_outputs')
    output_constraints = models.ManyToManyField('data.Constraint', related_name='tool_output_constraints', blank=True)
    
    machines = models.ManyToManyField(Machine)

    def __unicode__(self):
        if self.version:
            return u'%s v%s' % (self.label, self.version)
        else:
            return u'%s' % self.label
    
    def get_proxy(self, machine=None):
        """ Return a proxy to the instance of the tool on the chosen client's
            machine.
        """
        
        from edsa.clients.pyro import pyro_manager
        
        name_list = pyro_manager.get_names()
        random.shuffle(name_list)
        for item in name_list:
            if get_object_label(item[0]) == generate_object_label(get_subclass_instance(self)):
                if not machine:
                    return item[1].getAttrProxy()
                elif machine == get_machine_name(item[0]):
                    return item[1].getAttrProxy()
                
        return None
        
    def get_active_machines():
        """ Find a list of machines on which this tool can be run. """
        result = []
        from edsa.clients.pyro import pyro_manager
        name_list = pyro_manager.get_names()
        random.shuffle(name_list)
        for item in name_list:
            if get_object_label(item[0]) == generate_object_label(get_subclass_instance(self)):
                result.append(get_machine_name(item[0]))
        return result
        
    @staticmethod
    def get_available(specific_tools=[]):
        """ Fetch available tool instances, grouped by task ID.  Each instance
            is presented as a dictionary with 'machine_name' and 'version'
            keys.
        """
        from edsa.clients.pyro import pyro_manager
        
        #   Handle individual argument
        if isinstance(specific_tools, Tool):
            specific_tools = [specific_tools]
        
        name_list = pyro_manager.get_names()
        result = {}
        for name_uri in name_list:
            proxy_obj = name_uri[1].getAttrProxy()
            if hasattr(proxy_obj, '_tool'): 
                #   We have a valid tool on a remote machine.
                #   Get the data for this tool.
                if specific_tools:
                    tools = filter(lambda x: x.id == proxy_obj._tool.id, specific_tools)
                else:
                    tools = Tool.objects.filter(label=proxy_obj._tool.label)
                for tool in tools:
                    if tool.id not in result:
                        result[tool.id] = get_subclass_instance(tool)
                    if not hasattr(result[tool.id], 'instances'):
                        result[tool.id].instances = []
                    result[tool.id].instances.append({'machine_name': get_machine_name(name_uri[0]), 'version': proxy_obj._tool.version})
        return result
        
    def default_task(self):
        if Task.objects.filter(tool=self).exists():
            #   Return the newest existing task using this tool.
            return Task.objects.filter(tool=self).order_by('-id')[0]
        else:
            #   Make a new task using this tool that has no dependencies.
            task, created = Task.objects.get_or_create(tool=self)
            return task
            
    def get_log_table(self):
        """ Moved from Ian's view, edsa.views.logView """
        from edsa.log.models import Log
        x = self
        Inputs=x.inputs.all()
        Outputs=x.outputs.all()
        okie=Log.objects.all()
        last=x.id
        ToolLog=[]
        logger=Log.objects.all().order_by('-id')
        ToolLog=[]
        for k in range(len(logger)):
            if logger[k].tool_id==last:          
                ToolLog+=[logger[k].id]
                if len(ToolLog)>50:
                    break    
        colLabels=['ID','Start','Stop']
        if len(ToolLog) > 0:
            log=Log.objects.get(id=ToolLog[len(ToolLog)-1])
            colLabels+=[val.variable for val in log.inputs.all()]
            colLabels+=[val.variable for val in log.outputs.all()]
        table=[]
        table+= [colLabels]
        for i in range(len(ToolLog)):
            log=Log.objects.get(id=ToolLog[i])
            row = [log.id, log.start_time, log.end_time]
            row += [val.data for val in log.inputs.all()]
            row += [val.data for val in log.outputs.all()]
            table+=[row]
        return table

class RegisteredPythonModule(models.Model):
    """ Generic metadata needed for Python data processing blocks.
        This is used to register:
         - invokers and capturers for tools
    """
    
    module = models.CharField(max_length=100, help_text='A complete module reference that you can import in a Python shell, e.g. library.module.submodule.')
    class_name = models.CharField(max_length=40, help_text='The name of your Python class within that module.')
    documentation = models.TextField(blank=True, null=True, help_text='Documentation of your module.  Please be detailed!')
    
    #   Dictionary in JSON
    _default_params = models.TextField(default='{}', verbose_name='Default parameters', help_text='A JSON formatted dictionary of additional information that will be passed to your run() function.  Leave as "{}" if you don\'t know what this means.')
    
    def _get_default_params(self):
        return json.loads(self._default_params)
    def _set_default_params(self, params):
        self._default_params = json.dumps(params)
    default_params = property(_get_default_params, _set_default_params)

    def __unicode__(self):
        return u'%s.%s' % (self.module, self.class_name)

    def clean(self):
        """ Try to import the target class to make sure it's not a goof. """
        from django.core.exceptions import ValidationError
        try:
            self.get_class()
        except:
            raise ValidationError('Could not import the class you specified.')
            
    @staticmethod
    def register(class_path):
        """ Take a fully qualified class identifier and register it if it 
            doesn't already exist.
        """
        path_dir = class_path.strip().split('.')
        module_name = '.'.join(path_dir[:-1])
        class_name = path_dir[-1]
        qs = RegisteredPythonModule.objects.filter(module=module_name, class_name=class_name).order_by('-id')
        if qs.exists():
            return qs[0]
        else:
            result, created = RegisteredPythonModule.objects.get_or_create(module=module_name, class_name=class_name, _default_params='{}', documentation='')
            return result

    def get_class(self):
        mod = __import__(str(self.module), (), (), str(self.class_name))
        return getattr(mod, self.class_name)
        
    def get_instance(self, *args, **kwargs):
        return self.get_class()(*args, **kwargs)

processor_types =  ('invoker', 'capturer')
invoker_contexts = ('arguments', 'file', 'stdin')
capturer_contexts = ('file', 'stderr', 'stdout')
class VariableProcessor(models.Model):
    """ Metadata for a Python module used to process values before or after
        execution of tools.
    """
    
    module = models.ForeignKey(RegisteredPythonModule, help_text='Must be a class that implements the right interface for the selected processor type.')
    tool = models.ForeignKey('CommandLineTool')
    
    processor_type = models.CharField(max_length=100, help_text='Options: %s' % ', '.join(processor_types))
    context = models.CharField(max_length=100, help_text='Where the processor draws its I/O')
    variables = models.ManyToManyField('data.Variable')
    line_number = models.IntegerField(default=1)
    seq = models.IntegerField(default=0)
    
    #   Dictionary in JSON
    _params = models.TextField(default='{}', help_text='JSON formatted dictionary')
    
    def _get_params(self):
        return json.loads(str(self._params))
    def _set_params(self, params):
        self._params = json.dumps(params)
    params = property(_get_params, _set_params)

    def __unicode__(self):
        return u'%s for %s (variables: %s) line %s' % (self.processor_type, self.context, ', '.join([v.label for v in self.variables.all()]), self.line_number)

class CommandLineTool(Tool):
    """ A tool that runs commands in a shell on the target machine. """
    
    client_cmd = models.TextField(help_text='Enter one or more commands separated by line breaks.  These will be executed in a command line on the client.')
    
    #   Invokers and capturers stored on one field with accessor functions
    processors = models.ManyToManyField(RegisteredPythonModule, through=VariableProcessor)
    
    def _get_invokers(self, line=None):
        if line:
            return VariableProcessor.objects.filter(tool=self, processor_type='invoker', line_number=line).order_by('seq')
        else:    
            return VariableProcessor.objects.filter(tool=self, processor_type='invoker').order_by('seq')
    invokers = property(_get_invokers)
    def _get_capturers(self, line=None):
        if line:
            return VariableProcessor.objects.filter(tool=self, processor_type='capturer', line_number=line).order_by('seq')
        else:    
            return VariableProcessor.objects.filter(tool=self, processor_type='capturer').order_by('seq')
    capturers = property(_get_capturers)

class PythonTool(Tool):
    """ A tool that is executed by calling the run() function on the registered 
        Python class present on the target machine. 
    """
    
    module = models.ForeignKey(RegisteredPythonModule, help_text='Must be a class that implements the Python tool interface.')
    
class Task(models.Model):
    """ A tree of tool actions grouped together. """
    
    tool = models.ForeignKey(Tool, blank=True, null=True)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    def __unicode__(self):
        if self.tool:
            return u'Task: %s v%s (%d dependencies)' % (self.tool.label, self.tool.version, len(self
.all_dependencies()))
        else:
            return u'Task: no tool'
            
    @staticmethod
    def get_available(specific_tasks=[]):
        """ Fetch available task instances, grouped by task ID.  Each instance
            is presented as a dictionary with 'machine_name' and 'version'
            keys.
        """
        from edsa.clients.pyro import pyro_manager
        
        #   Handle individual item rather than list
        if isinstance(specific_tasks, Task):
            specific_tasks = [specific_tasks]
        
        name_list = pyro_manager.get_names()
        result = {}
        for name_uri in name_list:
            proxy_obj = name_uri[1].getAttrProxy()
            if hasattr(proxy_obj, '_tool'):
                #   We have a valid tool on a remote machine.
                #   Get all tasks that use this tool.
                if specific_tasks:
                    tasks = filter(lambda x: x.tool_id == proxy_obj._tool.id, specific_tasks)
                else:
                    tasks = Task.objects.filter(tool__label=proxy_obj._tool.label)
                for task in tasks:
                    if task.id not in result:
                        result[task.id] = get_subclass_instance(task)
                    if not hasattr(result[task.id], 'instances'):
                        result[task.id].instances = []
                    result[task.id].instances.append({'machine_name': get_machine_name(name_uri[0]), 'version': proxy_obj._tool.version})
        return result

    def process_label(self, label=None):
        """ Generate a timestamped label for a task run.
            Avoid collisions with existing labels. 
        """
        from edsa.log.models import Log
        
        if label:
            #   Check that the label has not already been used.
            #   If it has, append a number (i.e. 'myrun_1', 'myrun_2', ...)
            qs = Log.objects.filter(label__startswith=label)
            if qs.exists():
                try:
                    #   print 'List of label components: %s' % qs.order_by('-label').values_list('label', flat=True)[0].split('_')
                    last_log_id = int(qs.order_by('-label').values_list('label', flat=True)[0].split('_')[-1])
                except ValueError:
                    last_log_id = 0
                label = '%s_%03d' % (label, last_log_id + 1)
        else:
            #   If no string was provided, generate one including the tool name and
            #   the date (i.e. aero_test_20100514_4)
            cur_day = datetime.now().date()
            tool_day_label = '%s_%s' % (cur_day.strftime('%Y%m%d'), self.tool.label.replace(' ', '_'))
            #   Find unnamed runs of this tool on this day
            qs = Log.objects.filter(label__startswith=tool_day_label)
            #   Set label to use the next available number
            if qs.exists():
                try:
                    #   print 'List of label components: %s' % qs.order_by('-label').values_list('label', flat=True)[0].split('_')
                    last_log_id = int(qs.order_by('-label').values_list('label', flat=True)[0].split('_')[-1])
                except ValueError:
                    last_log_id = 0
                label = '%s_%03d' % (tool_day_label, last_log_id + 1)
            else:
                label = tool_day_label + '_1'
                
        return label

    def get_remote_tool(self, machine_name=None, version=None, local=False):
        """ Fetch the RemoteTool Pyro object wrapping a tool of the specified
            version, on the specified machine. 
            If local is True, instantiates the RemoteTool in this process.
        """
        #   Select the appropriate version of the tool to run
        if version:
            #   Fetch the desired version
            target_tool = Tool.objects.get(version=version, label=self.tool.label)
        else:
            #   If the version was not provided, get the newest one
            target_tool = Tool.objects.filter(label=self.tool.label).order_by('-id')[0]

        if not local:
            remote_tool = target_tool.get_proxy(machine_name)
        else:
            from edsa.clients.remote import RemoteTool
            remote_tool = RemoteTool(get_subclass_instance(target_tool))
            
        return remote_tool

    def run(self, handle_dependencies=False, machine_name=None, label=None, version=None, local=False):
        """ Run the specified task remotely.  If no machine_name is specified,
            one of the available machines will be chosen arbitrarily.  An error
            will be raised if the underlying tool is not available.
        """
        
        label = self.process_label(label)

        if handle_dependencies:
            for task in self.dependencies.all():
                #   Allow other machines to provide dependencies.
                #   TODO: make it possible to specify rules for which machines
                #         are used when following a dependency chain.
                task.run(handle_dependencies, None, label)

        remote_tool = self.get_remote_tool(machine_name, version, local)
        input_vals = [var.latest_value() for var in self.tool.inputs.all()]
    
        if remote_tool:
            result = remote_tool.run(input_vals, {}, task=self, label=label)
        else:
            #   TODO: raise a pretty error of some kind
            result = 'Error, server disconnected'
            pass
            
        return result

    def all_dependencies(self):
        result = []
        for dep in self.dependencies.order_by('id'):
            result += dep.all_dependencies()
            result.append(dep)
        return result

    def inputs(self):
        """ Find all inputs of tools in this task that are not supplied as 
            outputs by their dependencies.
        """
        result = set()
        result |= set(list(self.tool.inputs.all()))
        for task in self.dependencies.all():
            result -= set(list(task.tool.outputs.all()))
            result |= task.inputs()
        return result
        
    def outputs(self):
        """ Find all outputs of tools in this task that are not used as 
            inputs by their parents.
        """
        result = set()
        for task in self.dependencies.all():
            result |= set(list(task.tool.outputs.all()))
            result -= task.inputs()
        result |= set(list(self.tool.outputs.all()))
        return result

    def missing_inputs(self):
        """ TODO: Do something """
        return []

    def check_dependencies(self):
        """ Verify that the dependencies for this task are satisfied.
            Maybe this is the same as saying there are no newer values for the
            input variables than those generated by dependencies?
            Or would it mean that machines are available to execute the dependencies?
            TODO: Actually check something and return False if it fails.
        """
        return True

class StimulusTask(Task):
    """ A persistent module for automating repetition of Tasks.
        
        The run() function invokes the run() method of the registered module,
        which accepts a task, a dictionary of "global" parameters and a list
        of (variable, parameters) pairs.
    """
    module = models.ForeignKey(RegisteredPythonModule, help_text='A module that implements the Stimulus interface.')
    stimulus_variables = models.ManyToManyField('data.Variable')
    _variable_params = models.TextField(default='{}', verbose_name='Parameters for each variable involved in the stimulus', help_text='JSON formatted dictionary')
    
    def _get_variable_params(self):
        return json.loads(str(self._variable_params))
    def _set_variable_params(self, params):
        self._variable_params = json.dumps(params)
    variable_params = property(_get_variable_params, _set_variable_params)

    def __unicode__(self):
        if self.tool:
            return u'StimulusTask: %s, using %s (%d dependencies)' % (unicode(self.module), self.tool.label, self
.dependencies.count())
        else:
            return u'StimulusTask: %s, no tool' % unicode(self.module)

    def run(self, handle_dependencies=False, machine_name=None, label=None, version=None, local=False, params={}):
        """ Overrides Task.run() to delegate control of the RemoteTools to the 
            registered module.  The params argument may be used to override
            the default_params of the registered module.
        """
        label = self.process_label(label)
        def _run_task():
            #   TODO: See todos from main Task.run() function
            if handle_dependencies:
                for task in self.dependencies.all():
                    task.run(handle_dependencies, None, label)
            remote_tool = self.get_remote_tool(machine_name, version, local)
            input_vals = [var.latest_value() for var in self.tool.inputs.all()]
            if remote_tool:
                result = remote_tool.run(input_vals, {}, task=self, label=label)
            else:
                result = 'Error, server disconnected'
            return result
            
        #   Get all variables and zip them up with parameters
        variable_list = []
        for var in self.stimulus_variables.all():
            if var.label in self.variable_params:
                variable_list.append((var, self.variable_params[var.label]))
            else:
                variable_list.append((var, {}))
                
        #   Invoke the stimulus.  This may run the task multiple times.
        module_params = self.module.default_params
        module_params.update(params)
        result = self.module.get_instance().run(_run_task, variable_list, **module_params)

        return result
