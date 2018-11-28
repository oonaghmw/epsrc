import r2, nd, random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from dtlz import DTLZ1, DTLZ2
from scipy.optimize import minimize
#from pygmo import hypervolume

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

def weights_gen( k ) :
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
	return [ ( i/( k - 1 ), 1-i/( k-1 ) ) for i in range( k ) ]
	
def f(x):
	return (x[0], x[1])
	
def mutate_aux2( x, rate ):
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
	#CHANGE THIS
	if random.random() < rate:
		while True:
			x += np.random.normal(0) #edit variance?
			if x > 0 and x < 1:
				break
	return x
	
def mutate_aux( x, rate ):
	#CHANGE THIS
	if random.random() < rate:
		while True:
			x_ = np.random.normal(x, 0.25) #edit variance?
			if x_ > 0 and x_ < 1:
				x = x_
				break
	return x
	
def mutate( a, rate ):
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
	return tuple( map( lambda x: mutate_aux( x, rate ), a ) )
	
def dict_nondom(dict):
	A   = list((dict.keys()))
	ndom = nd.nondom( np.array( A) ) 
	A  = [ A[ j ] for j in ndom ]
	
	for k in dict.copy():
		if k not in A:
			del dict[k] #unsafe?
	return dict
	
	
def evo( X, f, W, z, rate, gens ):
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
	dict = { f(x): x for x in X }
	dict = dict_nondom(dict)
	
	#plt.scatter(list(zip(*dict))[0], list(zip(*dict))[1])
	#plt.show()
	
	r   = r2.r2( dict.keys(), W, z )
	r2s = [(0, r)]
	
	#plt.scatter(0, r)
	
	for i in range( gens ):
		a = random.choice( list(dict.keys()) ) 
		x = dict[a]
		#dict_ = dict.copy()
		x = mutate( x, rate ) 
		a2 = f(x)
		
		dict[a2] = x
		dict = dict_nondom(dict)
		
		r    = r2.r2( dict.keys(), W, z ) 
		#print(r_)
		
		"""
		if r_ < r: #r2 seems to only ever improve???
			dict = dict_ # is it even necessary? 
			# will dict ever need to be restored?
			r = r_
			#plt.scatter(i+1, r)
		
		if r_ > r:
			print('Something weird')
		r = r_
		"""
		r2s.append((i+1, r))
			
	plt.plot(list(zip(*r2s))[0], list(zip(*r2s))[1])
	plt.title("R2 value of front over generations")
	plt.xlabel("generation")
	plt.ylabel("R2 value")
	plt.show()		
	return dict, r
	
	
	
	
"""
fix types so that this is unecessary 
"""
def dtlz2_mod2(tup):
	dtlz2 = DTLZ2(M=2) 
	return tuple(dtlz2.evaluate(np.array(tup)))
	
def dtlz1_mod2(tup):
	dtlz1 = DTLZ1(M=2) 
	return tuple(dtlz1.evaluate(np.array(tup)))
	
def dtlz2_mod3(tup):
	dtlz2 = DTLZ2(M=3) 
	return tuple(dtlz2.evaluate(np.array(tup)))
	
def dtlz1_mod3(tup):
	dtlz1 = DTLZ1(M=3) 
	return tuple(dtlz1.evaluate(np.array(tup)))
	
#################	
	
def dtlz1_front(x):
	return (x, 0.5-x)
	
def dtlz2_front(x): 
	return (x, (1-x**2)**(1/2))
	
	
def curve_distance(f, point):
	front = list(map(f, np.arange(0, 1.01, 0.01)))
	
	#print(r2.r2(front, W, point))
	return r2.r2(front, W, point)
	
def curve_evaluate(f, points):
	r2s = 0
	for p in points:
		r2s += curve_distance(f, p)
	
	return r2s/len(points)
	

	
####################

	
if __name__ == "__main__": 

	X = [tuple(np.random.rand(3)) for j in range(15)]
	W = r2.dir_gen(200)
	d, r = evo(X, dtlz2_mod3, W, (0, 0, 0), 0.7, 500)
	
	