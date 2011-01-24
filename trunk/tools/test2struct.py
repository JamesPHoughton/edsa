class Test2Struct(object):
    def run(self, input_vars, **kwargs):

        """Structures code for EDSA test 2
        t_avg is average airfoil thickness
        W_fuse is the total weight suspended at the wing root
        c is root chord
        b is span
        eta_ac is the assumed aerodynamic center
        E is the elastic modulus of the wing material"""
        
        t_avg = input_vars['t_avg']
        W_fuse = input_vars['W_fuse']
        c = input_vars['c']
        b = input_vars['b']
        eta_ac = input_vars['eta_ac']
        E = input_vars['E']
	M_batt = input_vars['M_batt']
	S = input_vars['S']
        
        a = eta_ac*(S/c)/2.0                #aerodynamic center
        I = 1.0/12.0 * (S/b) * t_avg**3.0   #second moment of area
        G_wing = 0.5*(W_fuse+M_batt*9.8) * a**2.0 / (6.0*E*I) * (3.0*(S/c)/2.0 - a)  #tip deflection

        result = {'G_wing':G_wing}
        print 'Structures function computed %s' % result
        return result

