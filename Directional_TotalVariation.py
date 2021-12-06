
#%%
from cil.optimisation.functions import L2NormSquared, MixedL21Norm
from cil.optimisation.operators import DiagonalOperator, CompositionOperator,FiniteDifferenceOperator, IdentityOperator, BlockOperator
from cil.optimisation.algorithms import PDHG
from cil.utilities.display import show2D
from cil.utilities import dataexample
from cvxpy import *
from regularisers import dtv
import numpy as np
import matplotlib.pyplot as plt

#%%
# Load Data and resize
data = dataexample.CAMERA.get(size=(32, 32))

# Reference image
reference = data * 0.01

# Construct problem    
u_cvx = Variable(data.shape)

# fidelity
fidelity = sum_squares(u_cvx - data.array)   

# regulariser
eta = 0.1
alpha = 0.5
regulariser = alpha * dtv(u_cvx, reference, eta) 
constraints = []

obj =  Minimize( regulariser +  fidelity)
prob = Problem(obj, constraints)

# Choose solver (SCS is fast but less accurate than MOSEK)
res = prob.solve(verbose = True, solver = SCS, eps=1e-5)
#%%
# setup 2D directional TV denoising, using CIL and the PDHG algorithm

# image geometry
ig = data.geometry

# fidelity term
g = L2NormSquared(b=data)

# setup operator for directional TV
DY = FiniteDifferenceOperator(ig, direction=1)
DX = FiniteDifferenceOperator(ig, direction=0)

Grad = BlockOperator(DY, DX)
grad_ref = Grad.direct(reference)
denom = (eta**2 + grad_ref.pnorm(2)**2).sqrt()
xi = grad_ref/denom

A1 = DY - CompositionOperator(DiagonalOperator(xi[0]**2),DY) - CompositionOperator(DiagonalOperator(xi[0]*xi[1]),DX)
A2 = DX - CompositionOperator(DiagonalOperator(xi[0]*xi[1]),DY) - CompositionOperator(DiagonalOperator(xi[1]**2),DX)

operator = BlockOperator(A1, A2)

f = alpha * MixedL21Norm()

# use primal acceleration due to g being strongly convex
pdhg = PDHG(f = f, g = g, operator = operator, 
            max_iteration=500, update_objective_interval = 100, gamma_g = 1.)
pdhg.run(verbose=2)

#%%
# compare solution
np.testing.assert_almost_equal(pdhg.solution.array, u_cvx.value, decimal=3)

#%%
# print objectives
print("CVX objective = {}".format(obj.value))

print("CIL objective = {}".format(pdhg.objective[-1]))

# show middle line profiles
N, M = data.shape
plt.figure()
plt.plot(pdhg.solution.array[int(N/2)], label="CIL")
plt.plot(u_cvx.value[int(N/2)], label="CVXpy")
plt.legend()
plt.show()

show2D([pdhg.solution.array, u_cvx.value, np.abs(pdhg.solution.array - u_cvx.value)], num_cols = 3, origin="upper")


# %%
