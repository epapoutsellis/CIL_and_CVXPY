#%%

from cil.optimisation.functions.L2NormSquared import L2NormSquared
from cil.utilities import dataexample
from cvxpy import *
from regularisers import tv
from cil.optimisation.functions import TotalVariation
import numpy as np
import matplotlib.pyplot as plt
from cil.utilities.display import show2D

#%%
# Load Data and resize
data = dataexample.CAMERA.get(size=(32, 32))

#%%
# solution
u_cvx = Variable(data.shape)

#%%
# regularisation parameter
alpha = 0.1

#%%
# fidelity term
fidelity = 0.5 * sum_squares(u_cvx - data.array)   
regulariser = alpha * tv(u_cvx)

#%%
# objective
obj =  Minimize( regulariser +  fidelity)
prob = Problem(obj, constraints = [])

#%%
# Choose solver ( SCS, MOSEK(license needed) )
tv_cvxpy = prob.solve(verbose = True, solver = SCS)

# use TotalVariation from CIL (with Fast Gradient Projection algorithm)
TV = alpha * TotalVariation(max_iteration=100)
u_cil = TV.proximal(data, tau=1.0)

#%%
# compare solution
np.testing.assert_almost_equal(u_cil.array, u_cvx.value, decimal=3)

#%%
# print objectives
print("CVX objective = {}".format(obj.value))

f = 0.5*L2NormSquared(b=data)
cil_objective = TV(u_cil) + f(u_cil)
print("CIL objective = {}".format(cil_objective))

# show middle line profiles
N, M = data.shape
plt.figure()
plt.plot(u_cil.array[int(N/2)], label="CIL")
plt.plot(u_cvx.value[int(N/2)], label="CVXpy")
plt.legend()
plt.show()

show2D([u_cil.array, u_cvx.value, np.abs(u_cil.array - u_cvx.value)], num_cols = 3, origin="upper")

# %%
