from edsa.clients.pyro import pyro_manager

nl = pyro_manager.get_names()
print 'Found names: %s' % nl
for item in nl[1:]:
    obj = pyro_manager.get_object(item[0])
    print 'Found object: %s' % obj
    tool = obj._tool
    print 'Retrieved tool #%d: %s' % (tool.id, tool)


