from edsa.clients.models import *
from edsa.clients.invokers import *
from edsa.data.models import *

from edsa import settings

import numpy

def multi_open(filename, *args, **kwargs):
    for location in settings.EDSA_TOOL_PATH:
        try:
            file = open(location + '/' + filename, *args, **kwargs)
            #   print 'Located file: %s' % (location + '/' + filename)
            return file
        except:
            print 'Could not find: %s' % (location + '/' + filename)

    raise

#   Prepare variables
input_vars = {'alpha': 0.1,
              'Re': 5.0e5}
polar_file = multi_open('xfoil/dae11.dat')
polar_lines = polar_file.readlines()[1:]
r_par = []
for line in polar_lines:
    try:
        r_par.append([float(x.strip()) for x in line.strip().split(' ')])
    except:
        pass
        #   print 'Problematic line: %s' % line

r_par = numpy.array(r_par)

input_vars['r_par'] = r_par
#   print input_vars

polar_file.close()

#   Get tool
xfoil_tool = CommandLineTool.objects.filter(label='XFOIL').order_by('-version')[0]


#   Set values
input_vals = [var.latest_value() for var in xfoil_tool.inputs.all()]
for val in input_vals:
    if val.variable.label in input_vars:
        val.data = input_vars[val.variable.label]
        val.save()
    
#params = {'template': 'xfoil/xfoil_command_template.txt'}
params = {}
"""
#   Run invokers for line 1
input_state = InvokerState(values=input_vals, params=params)
for invoker in xfoil_tool._get_invokers(1):
    inv_kwargs = invoker.module.default_params
    inv_kwargs.update(invoker.params)
    inv_kwargs.update(params)
    invoker.module.get_instance().run(input_state, invoker.variables.all(), **inv_kwargs)

print input_state

xfoil_task = Task.objects.filter(tool=xfoil_tool).order_by('id')[0]
xfoil_task.run(local=True)
"""
