from edsa.clients.models import *
from edsa.data.models import *
from edsa.log.models import *
from edsa.tags.models import *

day = Unit.objects.get(name='day')
sec = BaseUnit.objects.get(name='second')
meter = BaseUnit.objects.get(name='meter')

degf = BaseUnit.objects.get(id=12)
degk = BaseUnit.objects.get(id=8)
degc = BaseUnit.objects.get(id=17)

#   Some tests of conversions

print '----------------'
print day.get_conversion(sec)
print '----------------'
print sec.get_conversion(day)
print '----------------'
print day.get_conversion(meter)
print '----------------'
print degf.get_conversion(degc)
print '----------------'
print degf.get_conversion(degk)
print '----------------'
print degc.get_conversion(degf)
print '----------------'
print degc.get_conversion(degk)
print '----------------'
print degk.get_conversion(degc)
print '----------------'
print degk.get_conversion(degf)

