from edsa.data.models import *
from edsa.clients.models import *

var=Variable.objects.get(label='test_file')
val=var.latest_value()
task = Task.objects.get(id=222)
"""
task.run(machine_name='rdc-mprice')
"""
tool = PythonTool.objects.get(id=20)
rt = task.get_remote_tool(machine_name='rdc-mprice')
rt.run([val], {}, task=task, label='test221')


