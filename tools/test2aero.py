
class Test2Aero(object):
    def run(self, input_vars, **kwargs):
        """Aerodynamics code for EDSA test 2
        V is velocity in meters per second
        alpha is angle of attack in radians
        b is wing span in meters
        c is root chord in meters
        LoverD is lift to drag ratio
        rho is air density in kg/m^3
        """

        V = input_vars['V']
        alpha = input_vars['alpha']
        b = input_vars['b']
        c = input_vars['c']
        LoverD = input_vars['LoverD']
        rho = input_vars['rho']

        # assumptions
        # Thin Airfoil Theory

        from math import pi

        CL = 2*pi*alpha;    # Lift Coefficient
        S = b*c;            # Wing Area
        L = .5*rho * V**2 * S * CL;     # Lift
        D = L / LoverD;     # Drag

        result = {'S':S, 'L':L, 'D':D}
        print 'Aero function computed: %s' % result
        return result

