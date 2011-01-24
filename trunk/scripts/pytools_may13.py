from edsa.data.models import *
from edsa.tags.models import *

from math import pi

variables = {   'V': 10.0,
                'alpha': 4.0 / 180 * pi,
                'b': 1.0,
                'c': 0.1,
                'LoverD': 10.0,
                'rho': 1.0,
                'E_batt': 4000.0,
                't_avg': 0.015,
                'W_fuse': 0.100,
                'eta_ac': 0.75,
                'E': 2.5e5,
             }


def_cat, created = DataCategory.objects.get_or_create(label='Wild guess')

for key in variables:
    #   Variables must be created in advance somewhere else
    var = Variable.objects.get(label=key)
    val = var.new_value(def_cat)
    val.data = variables[key]
    val.save()

