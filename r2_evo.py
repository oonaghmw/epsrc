import r2, nd, random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
#from deap import base, creator, tools #import warning??

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
	

"""
!!! COPY+PASTED FROM r2_tester !!!
Generate a pareto front. Points lie on the line x**p + y**p = 1.
Smaller values of p make a better pareto front.
Args:
	p 	 - number value greater than 0. 	
	step - number of points on the front. Cannot be negative.
Returns:
	List of the coordinates as a tuple of the points generated.
"""
def generate_pareto( p, step ):
	# guard statements - avoid p =< 0 ?
	x1 = np.linspace( 0, 1, step )
	x2 = ( 1 - x1**p ) ** ( 1/p )
	return list( zip( x1, x2 ) )
	
"""
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
	r	 - value of r2 for the resulting Pareto front !!!! NOT NECESSARY??
	As	 - list of each unique iteration of the Pareto front generated
"""
def evo( A, W, z, rate, gens ):
	As = [ A ]
	for i in range( gens ):
		r    = r2.r2( A, W, z )
		a    = random.choice( A ) #random or ordered?
		a_   = mutate( a, rate )
		A2   = A + [ a_ ]
		ndom = nd.nondom( np.array( A2 ) ) #make np in first place?
		A2   = [ A2[ x ] for x in ndom ]
		r_   = r2.r2( A2, W, z ) 
		if r_ < r: 
			A = A2
			r = r_
			As.append( A )
		
	return A, r, As
	
	
"""
Graph each unique version of the Pareto front given by the evolutionary algorithm on the same axis.
Args: 
	A	 - Initial Pareto front. List of tuples where tuple is the coordinates of a point.
	W 	 - weight vector required for R2. A list of tuples. ??????????????????????????????????????????
	z 	 - utopian point, tuple giving coordinates.
	rate - number giving rate of mutation
	gens - number of iterations to run algorithm for.
Returns: 
	none
"""
def pareto_evo( A, W, z = ( 0, 0 ), rate = 0.5, gens = 10 ):
	e, r, As = evo( A, W, z, rate, gens )
	
	for i in range( len( As ) ):
		A_ = sorted( As[ i ] )
		plt.plot( list( zip(* A_ ) )[0], list( zip(* A_ ) )[ 1 ] , alpha = 0.7, lw = 1 )
		plt.scatter( list( zip(* A_ ) )[0], list( zip(* A_ ) )[ 1 ] , alpha = 0.7, label = i+1 )
			
	plt.title("Evolution of Pareto front, {} iterations".format( gens ) )
	plt.xlabel( "f1(x)" )
	plt.ylabel( "f2(x)" )
	#plt.grid( True )
	plt.legend( title = "Generation", ncol = 2 ) #generation may be misleading since many more generations are not represented
	plt.show()
	
def r2_evo( A, W, z = ( 0, 0 ), rate = 0.5, gens = 10 ):
	r2s = [[0, r2.r2( A, W, z )]]
	for i in range( gens ):
		r    = r2.r2( A, W, z )
		a    = random.choice( A ) #random or ordered?
		a_   = mutate( a, rate )
		A2   = A + [ a_ ]
		ndom = nd.nondom( np.array( A2 ) ) #make np in first place?
		A2   = [ A2[ x ] for x in ndom ]
		r_   = r2.r2( A2, W, z ) 
		if r_ < r: 
			A = A2
			r = r_
			r2s.append([i+1, r])
	plt.scatter(list(zip(*r2s))[0], list(zip(*r2s))[1])
	plt.plot(list(zip(*r2s))[0], list(zip(*r2s))[1], lw = 1)
		
	plt.title("Evolution of R2 Value, {} iterations".format( gens ) )
	plt.xlabel( "Iteration" )
	plt.ylabel( "R2" )
	#plt.grid( True )
	plt.show()
	
def av_over_rate( A, W, z = ( 0, 0 ), gens = 10 ):
	av_r2s = []
	for i in np.arange(0, 1.1, 0.1):
		r2s = []
		for j in range(50):
			_, r, _ = evo( A, W, z, i, gens )
			r2s.append(r)
		av_r2s.append([i, np.mean(r2s)])
		
	plt.plot(list(zip(*av_r2s))[0], list(zip(*av_r2s))[1]) 
	plt.title("Average R2 over Mutation Rate")
	plt.xlabel("Mutation rate")
	plt.ylabel("Av. R2")
	plt.show()
	return av_r2s
	
def av_over_points( p, W, z = ( 0, 0 ), gens = 10 ):
	av_r2s = []
	for i in range(1, 10):
		A = generate_pareto(p, i)
		r2s = []
		for j in range(50):
			_, r, _ = evo( A, W, z, i, gens )
			r2s.append(r)
		av_r2s.append([i, np.mean(r2s)])
		
	plt.plot(list(zip(*av_r2s))[0], list(zip(*av_r2s))[1]) 
	plt.title("Average R2 over Initial no. Points")
	plt.xlabel("No. points")
	plt.ylabel("Av. R2")
	plt.show()
	return av_r2s
	
def av_over_weights( A, z = ( 0, 0 ), gens = 10 ):
	av_r2s = []
	for i in range(3, 11):
		W = weights_gen(i)
		r2s = []
		for j in range(50):
			_, r, _ = evo( A, W, z, i, gens )
			r2s.append(r)
		av_r2s.append([i, np.mean(r2s)])
		
	plt.plot(list(zip(*av_r2s))[0], list(zip(*av_r2s))[1]) 
	plt.title("Average R2 over no. weights")
	plt.xlabel("no. weights") ##### edit
	plt.ylabel("Av. R2")
	plt.show()
	return av_r2s
	
	
if __name__ == "__main__": 
	A = generate_pareto(1, 4)
	W = weights_gen(3)
	z = (0, 0)
	pareto_evo(A, W, z, 0.7, 500)
	
	r2_evo(A, W, z, 0.7, 500)

	#3d version 
	"""
	A = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.33, 0.33, 0.33)]
	W = r2.dir_gen( 3 ) #the weight changes - try to fix
	z = ( 0, 0, 0)
	print(r2.r2(A, W, z))
	A2, R2, As = evo(A, W, z, 0.5, 50)
	print(As)
	
	#fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')
	#ax.scatter(list(zip(*As))[0], list(zip(*As))[1], list(zip(*)
	#plt.show()
	"""