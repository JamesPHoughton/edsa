from edsa.clients.capturers import *
from edsa.data.models import *
from edsa.tags.models import *

default_category, created = DataCategory.objects.get_or_create(label='Wild guess')

x, created = Variable.objects.get_or_create(label='x')
xv = x.latest_value()

y, created = Variable.objects.get_or_create(label='y')
yv = y.latest_value()

z, created = Variable.objects.get_or_create(label='z')
zv = z.latest_value()

iv = CapturerState(stdout='4',values=[y.new_value(default_category)])

print unicode(iv)

sc=PlainStringCapturer()
sc.run(iv, [y])

print unicode(iv)



