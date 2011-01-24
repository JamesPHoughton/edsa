
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
""" EDSA remote tools

This file defines a class, RemoteTool, which wraps a Tool instance in a
Pyro object.  RemoteTool has one method, run(), which coordinates execution
of the tool.  If the tool is a PythonTool, its run() function is executed.
If the tool is a CommandLineTool, this procedure is followed:
1.  The required data values are fetched from the database and used to
    populate an InvokerState structure.
2.  The tool's invokers are run in sequence to prepare input for the tool
    in its native format.
3.  The tool's commands are executed in a shell on the machine hosting the 
    RemoteTool.
4.  The tool's capturers are run in sequence to extract the output of the
    tool commands into a CapturerState.
5.  Values from the CapturerState, and log information, are saved to the
    database.
"""

from edsa import settings

from edsa.clients.invokers import InvokerState, StringDump, PlainFileDump
from edsa.clients.capturers import CapturerState, PlainStringCapturer
from edsa.clients.models import Tool, CommandLineTool, PythonTool, Machine
from edsa.log.models import Log, CommandResult
from edsa.tags.models import DataCategory

import sys
import os
import subprocess
from datetime import datetime
from cStringIO import StringIO

import Pyro
import Pyro.core
import Pyro.naming

#   Add the specified directories to the path
if hasattr(settings, 'EDSA_TOOL_PATH'):
    for path in settings.EDSA_TOOL_PATH:
        sys.path.insert(0, path)

class RemoteObject(Pyro.core.ObjBase):
    """ Generic container for remote objects """
    def __init__(self, instance, *args, **kwargs):
        self._instance = instance
        Pyro.core.ObjBase.__init__(self, *args, **kwargs)

class RemoteFile(Pyro.core.ObjBase):
    def __init__(self, instance, *args, **kwargs):
        #   TODO: Check that the instance is on this machine!
        self._instance = instance
        self._file = None
        Pyro.core.ObjBase.__init__(self, *args, **kwargs)
        
    def close(self, *args, **kwargs):
        self._file.close(*args, **kwargs)
        self._file = None
        
    def __getattr__(self, attr):
        if self._file == None:
            self._file = open(settings.EDSA_STORAGE_DIR + self._instance.relative_path, 'r')
        try:
            return getattr(super(RemoteFile, self), attr)
        except:
            return getattr(self._file, attr)

class RemoteTool(Pyro.core.ObjBase):
    def __init__(self, tool=None, *args, **kwargs):
        self._tool = tool
        Pyro.core.ObjBase.__init__(self, *args, **kwargs)

    def run(self, values, params, task=None, user=None, label=None):
        """ Runs the stored tool on this machine using the provided parameters.
            Values is a list of DataValues for the tool's input variables.
            Params is a dictionary of parameters which are passed to invokers
            and capturers.
            
            The return value is the return value of the last command.  A Log
            object, including the values used and the raw input/output of the
            commands, is saved as part of the process.
        """

        if self._tool:
            #   Change to the working directory if desired 
            #   The commands may use subdirectories etc.
            orig_dir = os.getcwd()
            if hasattr(settings, 'EDSA_TOOL_WORKDIR'):
                os.chdir(settings.EDSA_TOOL_WORKDIR)
                
            #   Check input/output values
            #   TODO: Actually do this (apply constraints)
            in_vars = self._tool.inputs.all()
            out_vars = self._tool.outputs.all()
            
            output_category, created = DataCategory.objects.get_or_create(label='Result')
            output_values = []
            
            #   Start a log for this tool execution
            log = Log()
            log.start_time = datetime.now()
            log.machine = Machine.objects.get(label=settings.EDSA_MACHINE_NAME)
            log.user = user
            log.tool_id = self._tool.id
            log.task = task
            log.label = label
            log.save()
            for value in values:
                log.inputs.add(value)

            if isinstance(self._tool, CommandLineTool):
                
                #   Iterate through commands
                current_line = 1
                for cmd_line in self._tool.client_cmd.split('\n'):
                    cmd_rec = CommandResult()
                    
                    #   Prepare input for this line of the command script
                    self.input_state = InvokerState(values=values, params=params)
                    for invoker in self._tool._get_invokers(current_line):
                        inv_kwargs = invoker.module.default_params
                        inv_kwargs['context'] = invoker.context
                        inv_kwargs.update(invoker.params)
                        inv_kwargs.update(params)
                        invoker.module.get_instance().run(self.input_state, invoker.variables.all(), **inv_kwargs)
                    
                    #   Get the initial arguments that were already on the command line
                    cmd_initial = cmd_line.strip()
                    
                    #   Split the command into arguments, but don't break apart quoted areas
                    #   e.g.    echo "Hello world" -> ['echo', 'Hello world']
                    cmd_args = []
                    quoted_regions = cmd_initial.split('"')
                    for i in range(len(quoted_regions)):
                        if i % 2 == 0:
                            sub_args = quoted_regions[i].split(' ')
                            for arg in sub_args:
                                if len(arg.strip()) > 0:
                                    cmd_args.append(arg)
                        else:
                            cmd_args.append(quoted_regions[i])
                    
                    #   Add the arguments supplied from the invokers
                    cmd_args += self.input_state.arguments
                    
                    #   Save a summary of the command for the log
                    cmd_oneliner = ''

                    #   Temporary hack to allow Qprop to work.  -Michael
                    if len(cmd_args) == 2:
                        later_args = cmd_args.pop(1)
                        cmd_args += later_args.split(' ')
                        print cmd_args
                    #   End of hack

                    for arg in cmd_args:            
                        if ' ' in arg:
                            cmd_oneliner += '"%s" ' % arg
                        else:
                            cmd_oneliner += '%s ' % arg

                    cmd_rec.cmd = cmd_oneliner
                    print 'Executing: %s' % cmd_rec.cmd
                    
                    #   Run the command
                    cmd_process = subprocess.Popen(cmd_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    #   Store the immediate results of the command in the database
                    cmd_rec.stdin = self.input_state.stdin
                    (cmd_rec.stdout, cmd_rec.stderr) = cmd_process.communicate(self.input_state.stdin)
                    cmd_rec.retval = cmd_process.returncode
                    cmd_rec.save()
                    log.commands.add(cmd_rec)
                    
                    #   Capture output of this line into new values
                    output_values = [var.new_value(output_category) for var in out_vars]
                    for val in output_values:
                        val.supplier_id = self._tool.id
                        val.save()
                    self.output_state = CapturerState(values=output_values, params=params, files=self.input_state.files, stdout=cmd_rec.stdout, stderr=cmd_rec.stderr)
                    for capturer in self._tool._get_capturers(current_line):
                        cap_kwargs = capturer.module.default_params
                        cap_kwargs['context'] = capturer.context
                        cap_kwargs.update(capturer.params)
                        cap_kwargs.update(params)
                        capturer.module.get_instance().run(self.output_state, capturer.variables.all(), **cap_kwargs)

                    #   Clean up files
                    #   TODO: Add some option for archiving in folder named by log label or something
                    for filename in self.output_state.files:
                        os.remove(filename)

                    #   print unicode(self.input_state)
                    #   print unicode(self.output_state)
                    current_line += 1
    
                    
            elif isinstance(self._tool, PythonTool):
                
                #   TODO: What should the logging look like?  (Commands/return values)
                
                #   Stick the inputs in a dictionary
                input_data = {}
                for value in values:
                    input_data[value.variable.label] = value.data
                    
                #   Run the tool as specified in the RegisteredPythonModule
                output_data = self._tool.module.get_instance().run(input_data)
                
                #   Pull output values from the dictionary returned by the tool
                output_values = [var.new_value(output_category) for var in out_vars]
                for val in output_values:
                    val.supplier_id = self._tool.id
                    val.save()
                    if val.variable.label in output_data:
                        val.data = output_data[val.variable.label]
                        val.save()

            else:
                raise RuntimeError('Unsupported tool type')

            #   Save remaining information in the log
            for value in output_values:
                log.outputs.add(value)

            log.end_time = datetime.now()
            log.save()
            
            os.chdir(orig_dir)

            return 'Task completed'
            
        else:
            raise RuntimeError('Attempted to run nonexistent tool')
            
