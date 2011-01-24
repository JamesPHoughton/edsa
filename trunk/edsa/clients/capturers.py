
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
""" Capturers

Execution of a tool command results in output to stderr and stdout.  
EDSA needs to translate this output into DataValues which are stored
in the database.  To do so, the output is encoded in a CapturerState
which is passed through a sequence of Capturers.

The CapturerState is initialized with the shell output of the tool,
as well as a list of the input files that had been generated for the
tool and a set of uninitialized output values for each of the variables
that the tool provides.  The Capturers are sorted in ascending order by 
the 'seq' field of their VariableProcessor entries in the database.  Each 
Capturer provides a run() method which takes two arguments:
-   state: the current CapturerState
-   variables: the variables that it should try to capture

The run() method should look at the state.stdout and state.stderr
data and populate the state.values list with a list of values for the
desired output variables.
"""

import re

class CapturerState(object):
    def __init__(self, files={}, stdout='', stderr='', values=[], params={}):
        #   Apply default values without changing the defaults themselves if one is supplied
        if files is None:
            self.files = {}
        else:
            self.files = files
        if stdout is None:
            self.stdout = ''
        else:
            self.stdout = stdout
        if stderr is None:
            self.stderr = ''
        else:
            self.stderr = stderr
        if values is None:
            self.values = []
        else:
            self.values = values
        if params is None:
            self.params = {}
        else:
            self.params = params

    def __unicode__(self):
        return u'Files: %s\nStdout: %s\nStderr: %s\nValues: %s\nParams: %s\n' % (self.files, self.stdout, self.stderr, self.values, self.params)

class Capturer(object):
    """ This is the interface for Capturer, a category of RegisteredPythonModule
        that is invoked by the RemoteTool class in order to execute command
        line tools.  The arguments to run() are
        -   state: a CapturerState representing the current set of data that is
            being read from the output of the tool.
        -   variables: a list of variables that this capturer should pay attention
            to.  The capturer should not alter or use values for variables that
            are not included in this list.
        -   kwargs: A dictionary of global settings that may be defined by the
            author of the capturer (defaults should be stored in the default_params 
            of the RegisteredPythonModule).
    """
    def run(self, state, variables, **kwargs):
        raise NotImplementedError

class PlainStringCapturer(Capturer):
    """ A capturer that simply takes the output of the tool and saves it
        (as a string) into the value.
    """
    def run(self, state, variables, **kwargs):
        for var in variables:
            #   Find the value corresponding to that variable
            for value in state.values:
                if value.variable == var:
                    #   Use scalar floating point values by default
                    #   TODO: do something smarter here
                    value.data = float(state.stdout.strip())
                    value.save()

class RegexpCapturer(Capturer):
    """ A capturer that matches regular expressions against the output of the
        tool.  The standard output is checked by default.
    """
    def parse(self, data, state, variables, **kwargs):
        #   Get the expression from the 'regexp' argument
        result = re.search(kwargs['regexp'], data)
        
        group_counter = 0
        for val in state.values:
            if val.variable in variables:
                #   print 'Checking for matches on variable %s' % val.variable.label
                #   Check for named groups and assign values to the appropriate named variables.
                if val.variable.label in result.groupdict():
                    #   print 'Found named group result %s' % result.groupdict()[val.variable.label]
                    val.data = float(result.groupdict()[val.variable.label])
                    val.save()
                #   Assign remaining variables in order of unnamed groups?
                #   TODO: Fix this logic somewhat, it's going to be undesirable soon enough
                else:
                    if group_counter < len(result.groups()):
                        #   print 'Taking unnamed group result %s' % result.groups()[group_counter]
                        val.data = float(result.groups()[group_counter])
                        val.save()
                        group_counter += 1

    def run(self, state, variables, **kwargs):
        #   Read from a file if the filename is specified.
        if 'filename' in kwargs:
            file = open(kwargs['filename'], 'r')
            self.parse(file.read(), state, variables, **kwargs)
            file.close()
            state.files[kwargs['filename']] = []
        #   Otherwise, read from the standard output or standard error.
        else:
            if kwargs['context'] == 'stderr':
                self.parse(state.stderr, state, variables, **kwargs)
            else:
                self.parse(state.stdout, state, variables, **kwargs)
        
