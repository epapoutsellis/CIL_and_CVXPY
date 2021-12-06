

from cil.utilities import dataexample
from cvxpy import *
from regularisers import dtv
from ccpi.filters.regularisers import FGP_dTV


# Load Data and resize
data = dataexample.CAMERA.get(size=(32, 32))

# Reference image
reference = data * 0.01


# Construct problem    
u_cvx = Variable(data.shape)

# fidelity
fidelity = 0.5 * sum_squares(u_cvx - data.array)   

# regulariser
eta = 0.1
alpha = 0.5
regulariser = alpha * dtv(u_cvx, reference, eta) 
constraints = []

obj =  Minimize( regulariser +  fidelity)
prob = Problem(obj, constraints)

# Choose solver (SCS is fast but less accurate than MOSEK)
res = prob.solve(verbose = True, solver = SCS, eps=1e-5)