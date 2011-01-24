from edsa.data.models import *

def_cat, created = DataCategory.objects.get_or_create(label='Wild guess')

x, created = Variable.objects.get_or_create(label='x')
print x.latest_value()
try:
    x.current_data = 2
except:
    val = x.new_value(def_cat)
    val.data = 2
    val.save()
print x.latest_value()

y, created = Variable.objects.get_or_create(label='y')
try:
    y.current_data = 3.5
except:
    val = y.new_value(def_cat)
    val.data = 3.5
    val.save()
    
z, created = Variable.objects.get_or_create(label='z')
try:
    z.current_data = 1
except:
    val = z.new_value(def_cat)
    val.data = 1
    val.save()

