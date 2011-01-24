from edsa.clients.pyro import pyro_manager

nl = pyro_manager.get_names()

objects = []

for ne in nl:
    obj = ne[1].getAttrProxy()
    objects.append(obj)
    """
    if hasattr(obj, '_tool'):
        print '%s has tool' % obj
    else:
        print '%s has no tool' % obj
    """