import r2, nd, random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from dtlz import DTLZ2

"""
PSEUDOCODE

initialise A
Choose set of weightings W 
Choose utopian point z

while not converged: 
	a  <- solution from A 
	a' <- perturb(a) 
	
	if r2(A.append(a'), W, z) < r2(A, W, z):
		A = A.append(a')
	A <- nondom(A)
		
WRITE NONDOM(A) 
"""

"""
!!! Multiple versions in different modules - fix !!!
Generate a weights vector as a list with k weight tuples.
the weights in each tuple add to 1. Currently only 2 dimensions.
Args:
	k 	- the number of tuples of weights in the vector. Must be 
		  greater than 1. 
Returns:
	list with k elements. Each element is a tuple of length 2
	with positive float elements adding to 1. 
"""
def weights_gen( k ) :
	return [ ( i/( k - 1 ), 1-i/( k-1 ) ) for i in range( k ) ]
	
def f1(x):
	return x[0]*2

def f2(x):
	return x[1]*0.5
	
def f(x):
	return (f1(x), f2(x))
"""
To be called by mutate function. Randomly mutates a number x by 
adding a random number chosen from the range (-1, 1). The value
of the mutated number is greater than 0. Mutation occurs
with a probability given by the rate.
Warning: It is possible for return values to be negative if a 
negative number is passed in and not mutated.
Args:
	x	 - Number to be perturbed
	rate - Probability of mutation, effectively in the range [0, 1]
		   (Values outside of this range will work but are redundant)
Returns:
	x, the new mutated value derived from x. Either a value greater 
	than 0 or the original value of x.
"""	
def mutate_aux( x, rate ):
	if random.random() < rate:
		while True:
			x += random.choice( ( -1, 1 ) )*random.random()
			if x > 0:
				break
	return x
	
"""
Randomly mutates a tuple of numbers.
Uses mutate_aux on each element to derive its new value.
Warning: It is possible for values in returned tuple to be negative if
tuple with negative values is passed in and not mutated.
Args: 
	a	 - tuple of numbers 
	rate - float giving the probability that each element is mutated, 
		  effectively in range [0, 1]
Returns:
	the mutated tuple. Values are either greater than 0 or the original 
	values passed in.
"""
def mutate( a, rate ):
	return tuple( map( lambda x: mutate_aux( x, rate ), a ) )
	
def dict_nondom(dict):
	A   = list((dict.keys()))
	ndom = nd.nondom( np.array( A) ) 
	A  = [ A[ j ] for j in ndom ]
	
	for k in dict.copy():
		if k not in A:
			del dict[k] #unsafe?
	return dict
	
	
"""
IN PROCESS OF BEING ALTERED
Evolutionary algorithm which, given an initial Pareto front, uses the R2 indicator 
defined in the r2 module to evolve a better performing front, aiming to minimise the 
value given by the R2 indicator. Utilised nondom function.
Args:
	A 	 - initial Pareto front of non dominated points, a list of tuples giving the coordinates.
	W 	 - weight vector required for R2. A list of tuples.
	z 	 - utopian point, tuple giving coordinates.
	rate - number giving rate of mutation
	gens - number of iterations to run algorithm for.
Returna:
	A 	 - resulting Pareto front, list of tuples 
	r	 - value of r2 for the resulting Pareto front
	As	 - list of each unique iteration of the Pareto front generated
"""
def evo( X, f, W, z, rate, gens ):
	dict = { f(x): x for x in X}
	print('dict:', dict, '\n')
	dict = dict_nondom(dict)
	
	print('dict2:', dict, '\n')
	
	r   = r2.r2( dict.keys(), W, z )
	
	for i in range( gens ):
		a = random.choice( list(dict.keys()) ) 
		x = dict[a]
		dict_ = dict.copy()
		x = mutate( x, rate ) #USE NEW MUTATION FUNCTION gaussian
		a2 = f(x)
		dict_[a2] = x
		dict_ = dict_nondom(dict_)
		
		r_   = r2.r2( dict_.keys(), W, z ) 
		
		if r_ < r: #r2 seems to only ever improve???
			dict = dict_ # is it even necessary? 
			# will dict ever need to be restored?
			r = r_
			
	return dict, r
	
"""
fix types so that this is unecessary 
"""
def dtlz2_mod(tup):
	dtlz2 = DTLZ2(M=2) 
	return tuple(dtlz2.evaluate(np.array(tup)))
	
if __name__ == "__main__": 
	#negative values are occuring
	
	dtlz2 = DTLZ2(M=2) 
	X = [np.random.rand(2) for i in range(10) ]
	W = weights_gen(3)
	z = np.array((0,0))
	d, r = evo(X, dtlz2.evaluate, W, z, 0.8, 1000)
	print('\nd:', d, '\nr:', r, '\n')
	
	#plt.scatter(list(zip(*d))[0], list(zip(*d))[1])
	#plt.show()
	
	
	