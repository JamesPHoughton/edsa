from math import pi
    
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

struct_result = test2struct(t_avg, W_fuse, c, b, eta_ac, E)


print aero_result
print prop_result
print struct_result

