import scipy.sparse as sp
import numpy as np

def SparseMat_GradientOperator(shape, direction='forward', order=1, boundaries='Neumann', **kwargs):

    len_shape = len(shape)    
    allMat = dict.fromkeys(range(len_shape))
    discretization = kwargs.get('discretization',[1.0]*len_shape)

    if order == 1:

        for i in range(0,len_shape):

            if direction == 'forward':

                mat = 1/discretization[i] * sp.spdiags(np.vstack([-np.ones((1,shape[i])),np.ones((1,shape[i]))]), [0,1], shape[i], shape[i], format = 'lil')

                if boundaries == 'Neumann':
                    mat[-1,:] = 0
                elif boundaries == 'Periodic':
                    mat[-1,0] = 1

            elif direction == 'backward':

                mat = 1/discretization[i] * sp.spdiags(np.vstack([-np.ones((1,shape[i])),np.ones((1,shape[i]))]), [-1,0], shape[i], shape[i], format = 'lil')

                if boundaries == 'Neumann':
                    mat[:,-1] = 0
                elif boundaries == 'Periodic':
                    mat[0,-1] = -1

            tmpGrad = mat if i == 0 else sp.eye(shape[0])

            for j in range(1, len_shape):

                tmpGrad = sp.kron(mat, tmpGrad ) if j == i else sp.kron(sp.eye(shape[j]), tmpGrad )

            allMat[i] = tmpGrad

    else:
        raise NotImplementedError    

    return allMat