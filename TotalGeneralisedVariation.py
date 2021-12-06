#%%
from cil.optimisation.operators import GradientOperator, SymmetrisedGradientOperator, IdentityOperator, ZeroOperator, BlockOperator
from cil.optimisation.functions import MixedL21Norm, BlockFunction, L2NormSquared, ZeroFunction
from cil.optimisation.algorithms import PDHG
from cil.utilities import dataexample
from cvxpy import *
from regularisers import tgv
import numpy as np
import matplotlib.pyplot as plt
from cil.utilities.display import show2D

#%%
# Load Data and resize
data = dataexample.CAMERA.get(size=(32, 32))

# solution
u_cvx = Variable(data.shape)
w1_cvx = Variable(data.shape)
w2_cvx = Variable(data.shape)

# regularisation parameter
alpha0 = 0.1
alpha1 = 0.3

# fidelity term
fidelity = 0.5 * sum_squares(u_cvx - data.array)   
regulariser = tgv(u_cvx, w1_cvx, w2_cvx, alpha1, alpha0)

# objective
obj =  Minimize( regulariser +  fidelity)
prob = Problem(obj, constraints = [])

# Choose solver ( SCS, MOSEK(license needed) )
tv_cvxpy = prob.solve(verbose = True, solver = SCS)

#%%
# setup TGV denoising using CIL and the PDHG algorithm
ig = data.geometry

K11 = GradientOperator(ig)
K22 = SymmetrisedGradientOperator(K11.range)
K12 = IdentityOperator(K11.range)
K21 = ZeroOperator(ig, K22.range)
K = BlockOperator(K11, -K12, K21, K22, shape=(2,2) )

f1 = alpha1 * MixedL21Norm()
f2 = alpha0 * MixedL21Norm()
F = BlockFunction(f1, f2)
G = BlockFunction(0.5 * L2NormSquared(b=data), ZeroFunction())

sigma = 1./np.sqrt(12)
tau = 1./np.sqrt(12)

# Setup and run the PDHG algorithm
pdhg_tgv = PDHG(f=F,g=G,operator=K,
            max_iteration = 1000, sigma=sigma, tau=tau,
            update_objective_interval = 500)
pdhg_tgv.run(verbose = 2)

# compare solution
np.testing.assert_almost_equal(pdhg_tgv.solution[0].array, u_cvx.value, decimal=3)

#%%
# print objectives
print("CVX objective = {}".format(obj.value))
print("CIL objective = {}".format(pdhg_tgv.objective[-1]))

# show middle line profiles
N, M = data.shape
plt.figure()
plt.plot(pdhg_tgv.solution[0].array[int(N/2)], label="CIL")
plt.plot(u_cvx.value[int(N/2)], label="CVXpy")
plt.legend()
plt.show()

show2D([pdhg_tgv.solution[0].array, u_cvx.value, np.abs(pdhg_tgv.solution[0].array - u_cvx.value)], num_cols = 3, origin="upper")




