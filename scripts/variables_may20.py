from edsa.data.models import *

#   Initialize all variables needed for scripts
from math import pi

"""
V       = 10.0              # velocity in meters per second
alpha   = 4.0 / 180 * pi;   # angle of attack
b       = 1.0;              # wing span
c       = 0.1;              # root chord
LoverD  = 10.0;             # lift to drag ratio
rho     = 1.0;              # air density

aero_result = test2aero(V, alpha, b, c, LoverD, rho)

E_batt = 4000.0;            #energy stored in battery, in joules

prop_result = test2prop(V, aero_result['D'], E_batt)

t_avg = 0.015               # average airfoil thickness
W_fuse = 0.100              # fuselage weight
eta_ac = 0.75               # span-normalized aerodynamic center
E = 250000.0                # elastic modulus
"""

variables = [   ('b', 'm', 1.0),
                ('c', 'm', 0.1),
                ('alpha', 'rad', 4.0 / 180 * pi),
                ('V', 'm/s', 10.0),
                ('LoverD', ' ', 10.0),
                ('rho', 'kg/m^3', 1.0),
                ('S', 'm^2', None),
                ('L', 'N', None),
                ('D', 'N', None),
                ('E_batt', 'J', 4000.0),
                ('t_flight', 's', None),
                ('t_avg', 'm', 0.015),
                ('W_fuse', 'N', 0.100),
                ('eta_ac', ' ', 0.75),
                ('E', 'Pa', 2.5e5),
                ('G_wing', 'm', None),
                ('Re', ' ', None),
                ('r_par', ' ', None),
                ('M', ' ', 0),
            ]
            
def_cat, created = DataCategory.objects.get_or_create(label='Wild guess')            

for var_tup in variables:
    var, created = Variable.objects.get_or_create(label=var_tup[0])
    try:
        var.unit = BaseUnit.objects.get(symbol=var_tup[1])
    except BaseUnit.DoesNotExist:
        var.unit = Unit.objects.get(symbol=var_tup[1])
    
    print 'Variable %s: Latest value = %s' % (var, var.latest_value())
    
    val = var.latest_value()
    if not val:
        print '  New value needed!'
        val = var.new_value(def_cat)
    if var_tup[2]:
        val.data = var_tup[2]
    val.save()
    
    #    val = var.new_value(def_cat)

