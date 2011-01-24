
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
""" Invokers

Command line tools expect data to be supplied via stdin, command-line
arguments, and files.  If data is stored in files, the locations of those
files should be supplied somehow as well.   EDSA needs to populate these
input sources from DataValues which are stored in the database.  To do so,
the input is encoded in an InvokerState which is passed through a sequence 
of Invokers.

The InvokerState is initialized with the input values of the tool.
The Invokers are sorted in ascending order by the 'seq' field 
of their VariableProcessor entries in the database.  Each Invoker 
provides a run() method which takes two arguments:
-   state: the current InvokerState
-   variables: the variables that it should try to populate

The run() method should look at the state.values list and store three forms of
output in the state:
-   arguments (a list of strings)
-   files (a dictionary mapping filename -> list of variables in the file)
-   stdin (a string which is piped in to the command)
"""

import random

from edsa import settings

from django.template import loader, Template, Context

#   Each invoker is initialized with:
#   - the current arguments, file, stdin
#   - the list of variables it deals with
#   - the parameters passed as kwargs to the run() function

class InvokerState(object):
    def __init__(self, arguments=None, files=None, stdin=None, values=None, params=None):
        #   Apply default values without changing the defaults themselves if one is supplied
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments
        if files is None:
            self.files = {}
        else:
            self.files = files
        if stdin is None:
            self.stdin = ''
        else:
            self.stdin = stdin
        if values is None:
            self.values = []
        else:
            self.values = values
        if params is None:
            self.params = {}
        else:
            self.params = params

    def __unicode__(self):
        return u'Arguments: %s\nFilenames: %s\nStdin: %s\nValues: %s\nParams: %s\n' % (self.arguments, self.files, self.stdin, self.values, self.params)

    def get_value_or_filename(self, variable):
        """ If the desired variable has been written to a file, return the
            filename.  Otherwise, look for a value bound to that variable
            and return the value (or None if it wasn't found).  This is useful 
            when rendering templates containing links to data that may have 
            already been written to a file.
        """
        #   print 'Searching for variable %s' % variable
        for key in self.files:
            #   print 'Checking %s' % key
            if variable in self.files[key]:
                #   print 'Returning %s for file including %s' % (key, variable.label)
                return key
        for val in self.values:
            if val.variable == variable:
                #   print 'Returning direct data for %s' % variable.label
                return val.data
        #   print 'Could not find value for %s' % variable.label
        return None

class Invoker(object):
    """ This is the interface for Invoker, a category of RegisteredPythonModule
        that is invoked by the RemoteTool class in order to execute command
        line tools.  The arguments to run() are
        -   state: an InvokerState representing the current set of data that is
            ready to be passed into the tool.
        -   variables: a list of variables that this invoker should pay attention
            to.  The invoker should not alter or use values for variables that
            are not included in this list.
        -   kwargs: A dictionary of global settings that may be defined by the
            author of the invoker (defaults should be stored in the default_params 
            of the RegisteredPythonModule).
    """
    def run(self, state, variables, **kwargs):
        raise NotImplementedError


class StringDump(Invoker):
    """ A simple invoker that dumps the value data into an argument of the
        command.
    """
    def run(self, state, variables, **kwargs):
        for var in variables:
            #   Find the value corresponding to that variable
            for value in state.values:
                if value.variable == var:
                    state.arguments.append('%s' % state.get_value_or_filename(var))


class PlainFileDump(Invoker):
    """ A simple invoker that writes the data directly to a file
        in string form and adds that to the list of files present in
        the invoker state.  Some other invoker will need to provide the
        filename to the tool, either as an argument or on stdin.
    """
    def run(self, state, variables, **kwargs):
    
        #   Get a temporary filename
        filename = 'tmp_%06d.txt' % (random.randint(0, 999999))
        tmp_file = open(filename, 'w')
        
        for var in variables:
            #   Find the value corresponding to that variable
            for value in state.values:
                if value.variable == var:

                    #   Dump the variable to the file
                    tmp_file.write('%s\n' % value.data)
                    
        #   Save this in the list of files
        tmp_file.close()
        state.files[filename] = variables

class TemplateFileDump(Invoker):
    """ An invoker that merges the values of the specified variables
        into a string using the Django template language.  The template
        should be supplied as a 'template' argument to run().  If
        it is desired to write the output to a filename, the filename
        should be supplied as a 'filename' argument.
    """
    def run(self, state, variables, **kwargs):
        #   Fetch the template
        t = loader.get_template(kwargs['template'])
        context_dict = {}
        for var in variables:
            context_dict[var.label] = state.get_value_or_filename(var)
        
        #   Provide parameters as context variables if desired
        context_dict.update(kwargs)
        
        context = Context(context_dict)
        if 'filename' in kwargs:
            #   Write to file
            outfile = open(settings.EDSA_TOOL_WORKDIR + '/' + kwargs['filename'], 'w')
            outfile.write(t.render(context))
            outfile.close()
            
            #   Update invoker state so future invokers know which variables
            #   are present in the file
            state.files[kwargs['filename']] = variables
        else:
            #   Pipe to stdin by default, although it can be piped to arguments also
            if kwargs['context'].startswith('arg'):
                state.arguments += [t.render(context)]
            else:
                state.stdin += t.render(context)
        
