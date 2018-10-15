import math
from scipy.stats import norm #norm.cdf(x) # cool

# Norm CDF: https://www.johndcook.com/blog/cpp_phi/
# so this is just totally unnecessary # cool. 
def phi(x):
    # constants
    a1 =  0.254829592;
    a2 = -0.284496736;
    a3 =  1.421413741;
    a4 = -1.453152027;
    a5 =  1.061405429;
    p  =  0.3275911;
    
    # Save the sign of x
    sign = 1;
    if (x < 0):
        sign = -1;
    x = abs(x)/math.sqrt(2.0);
    
    # A&S formula 7.1.26
    t = 1.0/(1.0 + p*x);
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x);
    
    return 0.5*(1.0 + sign*y);


# both the same. awesome. 
y = phi(0.5)
print('phi: ' + str(y))

yy = norm.cdf(0.5)
print('pyth: ' + str(yy))