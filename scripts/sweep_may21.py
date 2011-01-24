from edsa.log.models import *
from edsa.utils.subclass import get_subclass_instance

from matplotlib.pyplot import *
import numpy

LOG_NAME = 'linsweep6'
INDEP_VARS = ['alpha']
DEP_VARS = ['C_L', 'C_D']
STYLES = {'C_L': 'r-', 'C_D': 'b-'}
OVERLAY_VARS = ['Re']

logs = Log.objects.filter(label=LOG_NAME)

result_list = []
for log in logs:
    task = get_subclass_instance(log.task)
    vals = {}
    if log.end_time:
        for val in log.inputs.all():
            if val.variable in task.stimulus_variables.all():
                vals[val.variable.label] = val.data
        for val in log.outputs.all():
            vals[val.variable.label] = val.data
        print vals
        result_list.append(vals)

#   Key in traces: tuple of values of overlay vars
traces = {}
for item in result_list:
    overlay_tup = tuple(item[label] for label in OVERLAY_VARS)
    if overlay_tup not in traces:
        traces[overlay_tup] = {}
    #   Key into trace: name of var
    for var_name in DEP_VARS + INDEP_VARS:
        if var_name not in traces[overlay_tup]:
            traces[overlay_tup][var_name] = []
        traces[overlay_tup][var_name].append(item[var_name])
 
print traces

#   1 plot: 2 axes
#   - C_D vs. alpha (red) overlaid for labeled Re
#   - C_L vs. alpha (blue) overlaid for labeled Re

fig_index = 1
for ind_var in INDEP_VARS:

    figure(fig_index)
    grid(color='k', linestyle='--')
    
    #   TODO: make labels follow true labels of independent/dependent vars
    xlabel('Alpha (rad)')
    ylabel('Coefficient (non-dimensional)')
    title('Lift and drag coefficients from XFOIL')

    for overlay_name in traces:
        overlay = traces[overlay_name]
        ind_data = numpy.array(overlay[ind_var])
        for var in DEP_VARS:
            trace_label = '%s at %s' % (var, ', '.join(['%s=%s' % (OVERLAY_VARS[i], overlay_name[i]) for i in range(len(OVERLAY_VARS))]))
            plot(ind_data, numpy.array(overlay[var]), STYLES[var], hold=True, label=trace_label)

    legend(loc='best')
    savefig('data_%s.pdf' % ind_var, bbox_inches='tight', pad_inches=0.25)
    show()

    fig_index += 1
