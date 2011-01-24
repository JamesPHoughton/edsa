class Test2Prop(object):
    def run(self, input_vars, **kwargs):

        """Propulsion code for EDSA test 2
        V is velocity in meters per second
        D is vehicle drag in N
        E_batt is battery capacity"""

        V = input_vars['V']
        D = input_vars['D']
        E_batt = input_vars['E_batt']

        T = D               #Thrust
        P = T * V           #Power
        t_flight = E_batt/P #Endurance

        result = {'t_flight':t_flight}
        print 'Propulsion function computed: %s' % result
        return result
        
