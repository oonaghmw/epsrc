import r2, nd, random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from dtlz import DTLZ1, DTLZ2
from scipy.optimize import minimize
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
""" 
	
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
			x_ = np.random.normal(x, 0.25)
			if x_ > 0 and x_ < 1:
				x = x_
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
	
"""
Performs the non-dom operation on a dictionary given that the points
for which the non dominated front must be found are given by the keys
of the dictionary.
Args:
	dict	- a dictionary where the keys are tuples of consistent 
			  length representing points in objective space. The
			  values are the associated points in decision space.
Returns:
	dictionary with the items with keys as dominated points removed.
"""
def dict_nondom(dict):
	A   = list((dict.keys()))
	ndom = nd.nondom( np.array( A) ) 
	A  = [ A[ j ] for j in ndom ]
	
	for k in dict.copy():
		if k not in A:
			del dict[k] #unsafe?
	return dict
	
	
"""
Evolutionary algorithm which, given an initial Pareto front, uses the R2 indicator 
defined in the r2 module to evolve a better performing front, aiming to minimise the 
value given by the R2 indicator. Utilised nondom function. Shows graph of the 
value of R2 for each generation.
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
	dict = { f(x): x for x in X }
	dict = dict_nondom(dict)
	
	r   = r2.r2( dict.keys(), W, z )
	r2s = [(0, r)]
	
	for i in range( gens ):
		a = random.choice( list(dict.keys()) ) 
		x = dict[a]
		x = mutate( x, rate ) 
		#a2 = f(x)
		a2 = f(np.array(x))
		a2 = tuple(a2)
		
		
		dict[a2] = x
		dict = dict_nondom(dict)
		
		r    = r2.r2( dict.keys(), W, z ) 
		
		r2s.append((i+1, r))
			
	plt.plot(list(zip(*r2s))[0], list(zip(*r2s))[1])
	plt.title("R2 value of front over generations")
	plt.xlabel("generation")
	plt.ylabel("R2 value")
	plt.show()		
	return dict, r
	
	
	
	
"""
Adaptation of method from the dtlz module to make more usable in 
EA. Uses tuple as argument for test function DTLZ2 with 2 objectives.
Args:
	- 	tuple representing point in decision space
Returns:
	- 	2D tuple representing point transformed in objective space 
		by DTZL2
"""
def dtlz2_mod2(tup):
	dtlz2 = DTLZ2(M=2) 
	return tuple(dtlz2.evaluate(np.array(tup)))
	
"""
Adaptation of method from the dtlz module to make more usable in 
EA. Uses tuple as argument for test function DTLZ1 with 2 objectives.
Args:
	- 	tuple representing point in decision space
Returns:
	- 	2D tuple representing point transformed in objective space 
		by DTZL1
"""	
def dtlz1_mod2(tup):
	dtlz1 = DTLZ1(M=2) 
	return tuple(dtlz1.evaluate(np.array(tup)))

"""
Adaptation of method from the dtlz module to make more usable in 
EA. Uses tuple as argument for test function DTLZ2 with 3 objectives.
Args:
	- 	tuple representing point in decision space
Returns:
	- 	3D tuple representing point transformed in objective space 
		by DTZL2
"""	
def dtlz2_mod3(tup):
	dtlz2 = DTLZ2(M=3) 
	return tuple(dtlz2.evaluate(np.array(tup)))
	

"""
Adaptation of method from the dtlz module to make more usable in 
EA. Uses tuple as argument for test function DTLZ1 with 3 objectives.
Args:
	- 	tuple representing point in decision space
Returns:
	- 	3D tuple representing point transformed in objective space 
		by DTZL1
"""	
def dtlz1_mod3(tup):
	dtlz1 = DTLZ1(M=3) 
	return tuple(dtlz1.evaluate(np.array(tup)))
	
#################	

"""
Gives a coord point for 2D DTZL1.
Args: 
	-	number x 
Returns:
	- 	associated coordinate for x given DTZL1 as a tuple
"""
def dtlz1_front(x):
	return (x, 0.5-x)

"""
Gives a coord point for 2D DTZL2.
Args: 
	-	number x 
Returns:
	- 	associated coordinate for x given DTZL2 as a tuple
"""	
def dtlz2_front(x): 
	return (x, (1-x**2)**(1/2))
	
"""
Function to approximate R2 distance between the plot of a function 
and a given point. Models plot of function for x values [0, 1].
Args:
	-	function to model and find distance to point
	- 	a point as a tuple of numbers.
Returns:
	-	numerical value giving approximate R2 distance between
		point and plot of function in interval [0, 1].
"""
def curve_distance(f, point):
	front = list(map(f, np.arange(0, 1.01, 0.01)))
	return r2.r2(front, W, point)
	
"""
Finds the average distance given by curve_distance between the
plot of the fiven function and the list of points.
Args: 
	-	function to model and find distance to points
	- 	list of points as tuples of numbers.
Returns:
	-	numerical value giving av. approximate R2 distance between
		points and plot of function in interval [0, 1].
"""
def curve_evaluate(f, points):
	r2s = 0
	for p in points:
		r2s += curve_distance(f, p)
	
	return r2s/len(points)

	
if __name__ == "__main__": 

	X = [tuple(np.random.rand(3)) for j in range(15)]
	
	W = r2.dir_gen(200)
	d, r = evo(X, dtlz2_mod21, W, (0, 0, 0), 0.7, 100)
	
	