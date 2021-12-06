from cil.utilities import dataexample
from cvxpy import *
from regularisers import tv
from cil.optimisation.functions import TotalVariation
import numpy

# Load Data and resize
data = dataexample.CAMERA.get(size=(32, 32))

# set up TV denoising 

# unknown  
u_cvx = Variable(data.shape)

# regularisation parameter
alpha = 0.1

# fidelity term
fidelity = 0.5 * sum_squares(u_cvx - data.array)   
regulariser = alpha * tv(u_cvx)

# objective
obj =  Minimize( regulariser +  fidelity)
prob = Problem(obj, constraints = [])

# Choose solver ( SCS, MOSEK(license needed) )
tv_cvxpy = prob.solve(verbose = True, solver = SCS)

# use TotalVariation from CIL
TV = alpha * TotalVariation(max_iteration=100)
u_cil = TV.proximal(data, tau=1.0)

# compare solution
numpy.testing.assert_almost_equal(u_cil.array, u_cvx.value, decimal=3)



