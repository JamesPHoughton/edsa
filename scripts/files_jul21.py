from edsa.data.models import *

def_cat, created = DataCategory.objects.get_or_create(label='Wild guess')

fv = FileValue.objects.all()[0]
obj = fv.cast()

print 'Cast object: %s' % obj.__dict__

print 'File contents: %s' % obj.contents

#   Save the FileValue in a DataValue for variable 'test_file'
test_file = Variable.objects.get(label='test_file')
val = test_file.new_value(def_cat)
val.data = obj
val.save()
print val


raw_input('Reset pyro and then hit enter to continue...')

print 'Retrieving file %s again' % obj
obj = val.data
print obj.contents
