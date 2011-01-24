
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
""" EDSA Log models

The purpose of these models is to provide a detailed record of all tool
executions.  This is useful for collaborative purposes (i.e. seeing what
your coworkers have been up to) as well as debugging the tool.  

The Log model stores some common-sense metadata for each tool execution.
This includes references to the input values that were provided for (and
output values that were generated by) the tool, as well as a label that
can be provided in advance by the user or automatically generated.

Python tools produce no log information besides the output variables they
generate.  Command line tools may execute one or more shell commands, 
the results of which are stored in the CommandResult model.
"""

from django.db import models

from edsa.tags.models import Tag
from edsa.clients.models import EDSAUser, Tool, Task, Machine
from edsa.data.models import DataValue
 
class CommandResult(models.Model):
    """ A complete description of a single command line execution. """
    
    cmd = models.TextField(verbose_name='Command executed')
    stdin = models.TextField(blank=True, null=True)
    stdout = models.TextField(blank=True, null=True)
    stderr = models.TextField(blank=True, null=True)
    retval = models.IntegerField()

    def __unicode__(self):
        return u'%s -> returned %s' % (self.cmd, self.retval)

class Log(models.Model):
    """ A description of what happened when a particular task was run. """
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(EDSAUser, blank=True, null=True)
    tool = models.ForeignKey(Tool, blank=True, null=True)
    task = models.ForeignKey(Task, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    commands = models.ManyToManyField(CommandResult, editable=False)
    machine = models.ForeignKey(Machine, null=True)
    inputs = models.ManyToManyField(DataValue, related_name='logs_input', editable=False)
    #   This could be a ForeignKey from DataValue, but for symmetry
    #   I'm going to leave it here for now.   - Michael P
    outputs = models.ManyToManyField(DataValue, related_name='logs_output', editable=False)
    
    def __unicode__(self):
        if self.task:
            return u'%s: %s - %s' % (self.task.tool.label, self.start_time, self.end_time)
        elif self.tool:
            return u'%s: %s - %s' % (self.tool.label, self.start_time, self.end_time)
        else:
            return u'No tool specified'
    
