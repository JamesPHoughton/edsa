from edsa.clients.models import Tool, CommandLineTool, PythonTool
from edsa.data.models import *
from edsa.tags.models import *

import sys
sys.path.insert(0, '/home/price/projects/edsa/daemons')
from common import EDSARemoteTool

tool = CommandLineTool.objects.get(label='Dummy program')

remote_tool = EDSARemoteTool(tool)

input_vals = [var.latest_value() for var in tool.inputs.all()]
print remote_tool.run(input_vals, {})
"""
tool = PythonTool.objects.get(label='Test 2 aerodynamics code (Python)')

default_category, created = DataCategory.objects.get_or_create(label='Wild guess')

remote_tool = EDSARemoteTool(tool)

V = Variable.objects.get(label='V').new_value(default_category)
alpha = Variable.objects.get(label='alpha').new_value(default_category)
b = Variable.objects.get(label='b').new_value(default_category)
c = Variable.objects.get(label='c').new_value(default_category)
LoverD = Variable.objects.get(label='LoverD').new_value(default_category)
rho = Variable.objects.get(label='rho').new_value(default_category)

V = Variable.objects.get(label='V').latest_value()
alpha = Variable.objects.get(label='alpha').latest_value()
b = Variable.objects.get(label='b').latest_value()
c = Variable.objects.get(label='c').latest_value()
LoverD = Variable.objects.get(label='LoverD').latest_value()
rho = Variable.objects.get(label='rho').latest_value()

V.data = 10
alpha.data = 0.01
b.data = 1
c.data = 0.1
LoverD.data = 10
rho.data = 1

input_vals = [V, alpha, b, c, LoverD, rho]
for val in input_vals:
    val.save()
    
remote_tool.run(input_vals, {})
"""
