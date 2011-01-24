
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
from clients.models import Tool,Task
from log.models import Log
from data.models import BaseUnit,Variable,DataValue
from clients.forms import RunStimVarGraph




def execute():
    y=Task.objects.all()
    z=Task.objects.get(id=len(y))
    ToolID=z.tool_id
    x=Tool.objects.get(id=ToolID)
    Inputs=x.inputs.all()
    for i in range(len(Inputs)):
        if 'input_'+str(Inputs[i].description) in request.GET:             
            (Variable.objects.get(id=Inputs[i].id)).current_data=(request.GET['input_'+str(Inputs[i].description)])
    RUNIT=z.run()
    Outputs=x.outputs.all()
    results=[]
    for i in range(len(Outputs)):
        results+=[str(Outputs[i])+' = '+str((Variable.objects.get(id=Outputs[i].id)).current_data)]

    return results

def Display_Opt():
    y=Task.objects.all()
    z=Task.objects.get(id=len(y))
    ToolID=z.tool_id
    x=Tool.objects.get(id=ToolID)
    Inputs=x.inputs.all()
    Outputs=x.outputs.all()
    colLabels=['ID','Start','Stop']
    table=[Log.id,Log.start_time,Log.end_time]

    for i in range(len(Inputs)):
        table+=Inputs[i].get_data
        colLabels+=[str(Inputs[i].description)]
    for j in range(len(Inputs)):
        table+=Outputs[j].get_data
        colLabels+=[str(Outputs[j].description)]

    the_table = pylab.table(cellText=table,
                  colLabels=colLabels,
                  loc='center')
    pylab.xticks([])
    pylab.yticks([])
    pylab.box()
    pylab.savefig('media/table.png')
    pylab.clf()

    
    
