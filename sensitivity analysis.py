import math
from sympy import *

z = symbols("z")
cos_x = 1/2
sin_x = 1/2
aij = 10
print(integrate(1/(3.14/exp(z/3.14)+1/4*cos_x+math.sqrt(3)/4*sin_x), (z, 0, aij)))