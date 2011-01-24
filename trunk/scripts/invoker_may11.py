from edsa.clients.invokers import *
from edsa.data.models import *

x, created = Variable.objects.get_or_create(label='x')
xv = x.latest_value()

y, created = Variable.objects.get_or_create(label='y')
yv = y.latest_value()

z, created = Variable.objects.get_or_create(label='z')
zv = z.latest_value()

iv = InvokerState(values=[xv,yv,zv])

print unicode(iv)

sd = StringDump()
fd = PlainFileDump()
sd.run(iv, [x])
fd.run(iv, [y,z])

print unicode(iv)



