from edsa.clients.models import *
from edsa.data.models import *
from edsa.log.models import *
from edsa.tags.models import *

import numpy

day = Unit.objects.get(name='day')
sec = BaseUnit.objects.get(name='second')
meter = BaseUnit.objects.get(name='meter')

me = EDSAUser.objects.get(username='price')
cat, created = DataCategory.objects.get_or_create(label='Wild guess')

t_x = Variable.objects.get(label='t_x')
t_x_val = t_x.latest_value()
if t_x_val is None:
    t_x_val = DataValue(category=cat, variable=t_x)
    
t_x_val.data = 5
t_x_val.save()

print 'Current data: %s (%s)' % (t_x.current_data, t_x_val.timestamp)
t_x.current_data = numpy.matrix(numpy.linspace(1.,3.,4)).T * numpy.matrix(numpy.linspace(-2.
,2.,4))
print 'Current data: %s (%s)' % (t_x.current_data, t_x_val.timestamp)

