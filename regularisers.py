from  SparseMat_GradientOperator import SparseMat_GradientOperator
from cvxpy import *


def tv(u, isotropic=True, direction = "forward", boundaries = "Neumann"):
        
    G = SparseMat_GradientOperator(u.shape, direction = direction, order = 1, boundaries = boundaries)        
    DX, DY = G[1], G[0]
  
    if isotropic:
        return sum(norm(vstack([DX @ vec(u), DY @ vec(u)]), 2, axis = 0))
    else:
        return sum(norm(vstack([DX @ vec(u), DY @ vec(u)]), 1, axis = 0))

def tgv(u, w1, w2, alpha0, alpha1, boundaries = "Neumann"):

    G1 = SparseMat_GradientOperator(u.shape, direction = 'forward', order = 1, boundaries = boundaries)  
    DX, DY = G1[1], G1[0]

    G2 = SparseMat_GradientOperator(u.shape, direction = 'backward', order = 1, boundaries = boundaries) 
    divX, divY = G2[1], G2[0]
  
    return alpha0 * sum(norm(vstack([DX @ vec(u) - vec(w1), DY @ vec(u) - vec(w2)]), 2, axis = 0)) + \
           alpha1 * sum(norm(vstack([ divX @ vec(w1), divY @ vec(w2), \
                                      0.5 * ( divX @ vec(w2) + divY @ vec(w1) ), \
                                      0.5 * ( divX @ vec(w2) + divY @ vec(w1) ) ]), 2, axis = 0  ) )
       

def dtv(u, reference, eta, isotropic=True, direction = "forward", boundaries = "Neumann"):
        
    G = SparseMat_GradientOperator(u.shape, direction = direction, order = 1, boundaries = boundaries)         
    DX, DY = G[1], G[0]
    
    # gradient for reference image
    tmp_xi_x = DX@vec(reference.array)
    tmp_xi_y = DY@vec(reference.array)    
    denom = sqrt(tmp_xi_x**2 + tmp_xi_y**2 + eta**2)

    # compute field xi
    xi_x = tmp_xi_x/denom
    xi_y = tmp_xi_y/denom
    
    # gradient for u
    u_x = DX@vec(u)
    u_y = DY@vec(u) 
    
    inner_prod = multiply(u_x,xi_x) + multiply(u_y,xi_y)
    z1 = u_x - multiply(inner_prod,xi_x)
    z2 = u_y - multiply(inner_prod,xi_y)
    z = vstack([z1, z2])
    
    if isotropic:
        return sum(norm( z, 2, axis = 0))
    else:
        return sum(norm( z, 1, axis = 0))        