
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

import copy

class Stimulus(object):
    """ This is the interface for Stimulus, a category of RegisteredPythonModules
        that is invoked by the StimulusTask model.
        The arguments to run() are:
        -   task_function: A callable which represents the task to be stimulated.
        -   variable_list: An iterable of (variable, params) pairs, where in each
            pair 'variable' is a Variable object and 'params' is a dictionary of
            parameters relevant to that variable.
        -   kwargs: A dictionary of global settings that may be defined by the
            author of the stimulus (defaults should be stored in the default_params 
            of the RegisteredPythonModule).
    """
    def run(self, task_function, variable_list, **kwargs):
        raise NotImplementedError
        
class SingleRun(Stimulus):
    """ A simple stimulus that tests the interface by running the target task
        once. 
    """
    def run(self, task_function, variable_list, **kwargs):
        return task_function()
        
class LinearSweep(Stimulus):
    """ A stimulus that sweeps the variables that are passed in along with
        start, end, and num_points parameters and runs the target task
        at each point.  The Cartesian product of all variable sets is
        explored.
    """
    def product(self, initial_entries, new_var, start, end, num_points):
        """ Helper function to assist with building up a Cartesian product. """
        new_entries = []
        point_values = [start + i * (end - start) / (num_points - 1) for i in range(num_points)]
        for entry in initial_entries:
            for val in point_values:
                new_dict = copy.copy(entry)
                new_dict[new_var] = val
                new_entries.append(new_dict)
        return new_entries
    
    def run(self, task_function, variable_list, **kwargs):
        
        result = 'No stimulus points specified'
        
        #   Perform Cartesian product of variable ranges
        entries = [{}]
        for var_tup in variable_list:
            var = var_tup[0]
            var_params = var_tup[1]
            if ('start' in var_params) and ('end' in var_params) and ('num_points' in var_params):
                entries = self.product(entries, var, var_params['start'], var_params['end'], var_params['num_points'])
        
        #   Execute tool for each combination of stimulus values
        for entry in entries:
            print 'Running task for stimulus entry: %s' % entry
            #   Set values to reflect this entry
            for var in entry:
                var.current_data = entry[var]
            
            #   Run the task
            result = task_function()
        
        return result
