import math

v = 
delta_v = 
a = 
delta_a = 
rl = 
delta_rl = 



#FOR R_A
uncert_ra = math.sqrt( ((delta_v/v) ** 2) + ((delta_a/a) ** 2) + (delta_rl ** 2))

#FOR R_V
uncert_rv = math.sqrt( ((delta_rl/rl) ** 2) + ((delta_a/a) ** 2) + (1 + (a ** 2)))

