###########################################################################
############################### Dirichlet ################################
###########################################################################
##
## o author: Richard Everson (R.M.Everson@exeter.ac.uk)
## o created: 2008-11-20 20:47:15+00:00
## o last modified: $Date$
## o keywords: 
## o license: 


import numpy
import numpy.random

def randDirichlet(alpha, N=1):
    """
    Generate samples from a Dirichlet density with parameters given by the
    vector alpha. If N > 1, then an 2D array is returned with each row
    being a sample
    """
    # Each sample is just a draw from a gamma density with shape parameter
    # alpha_i and scale parameter 1, normalised by the sum of the draws in
    # that row.
    K = len(alpha)
    if K < 2:
        raise ValueError('Dirichlet order must be at least 2')
    
    if N == 1:
        x = numpy.zeros(K, 'd')
        for i in range(K):
            x[i] = numpy.random.gamma(alpha[i])
        x /= x.sum()
    else:
        x = numpy.zeros((N,K), 'd')
        for i in range(K):
            x[:,i] = numpy.random.gamma(alpha[i], size=(N,))
        #x /= numpy.reshape(numpy.repeat(x.sum(axis=1), K), (N,K))
        x /= x.sum(axis=1)[:,numpy.newaxis]
    return x

if __name__ == "__main__":
    # Minimal tests 

    alpha = numpy.asarray([2, 1, 3], 'd')
    N = 1000
    z = numpy.zeros((N, len(alpha)), 'd')
    for n in range(N):
        z[n] = randDirichlet(alpha)
    
    print('Single samples')
    print('Mean     ', z.mean(axis=0))
    print('Should be', alpha/alpha.sum())

    print()
    z = randDirichlet(alpha, N)
    print('Multiple samples')
    print('Mean     ',  z.mean(axis=0))
    print('Should be', alpha/alpha.sum())

            
        
