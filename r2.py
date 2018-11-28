import numpy.random as npr
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
"""				
Improvement is indicated by decrease in r2
A 						-> solution set of points on the parato front
W (or capital lambda) 	-> set of weights w (or lambda)
z (or z*) 				-> utopian point
m 						-> number of individual weights w in W

_max = max( [ W[ i ] * abs( z[ i ] - a[ i ] ) for i in range( m ) ])
_min = min( [ _max for a in A ] )
_sum = sum( [ _min for w in W ] )
R2 = _sum/len(W)
"""

def generate_pareto( p, step ):
	"""
	Generate sample Pareto fronts which, intuitively, we can judge the effectiveness of, 
	to test that the R2 indicator is behaving as expected, These take the form
	f_1(x)^p + f_2(x)^p = 1 
	We know the quality of the Pareto front should decrease as front improves, and therefore 
	R2 should decrease as p decreases. 
	The points are evenly distributed across one variable.
	Args:
		p	- number value to define curve. Larger p makes for larger R2. p = 1 gives a 
			straight line between (0, 1) and (1, 0), p = 2 gives the line segment of a circle
			radius 1 centre at the origin between (0, 1), (1, 0).
		step- number of points there should be making up the front. 
	Returns:
		list of tuples representing the set of 2D points making up the front.
	"""
	x1 = np.linspace( 0, 1, step )
	x2 = ( 1 - x1**p ) ** ( 1/p )
	return list( zip( x1, x2 ) )
	
def graph_front( front, p ):
	"""
	Plot a set of points/front to be used alongside fronts generated by generate_pareto.
	Args:
		front	- the set of points, list of tuples representing 2D coords
		p 		- for printing the title, the p value associated with the function 
				used to generate the front in generate_pareto.
	Returns:
		none
	"""
	plt.scatter( list( zip(* front ) )[0], list( zip(* front ) )[1] )
	plt.grid( True )
	plt.xlabel( "f1(x)" )
	plt.ylabel( "f2(x)" )
	plt.title( "A for when p = {}".format( p ) )
	plt.show()
	
def weights_gen(k) :
	"""
	Generate a list of 2D weight vectors as a list of k tuples.
	The weights in each tuple add to 1, and are evenly distributed 
	over the weight space.
	Args:
		k 	- the number of tuples of weights in the vector. Must be 
			greater than 1. 
	Returns:
		list with k elements. Each element is a tuple of length 2
		with positive float elements adding to 1. 
	"""
	return [(i/(k-1), 1-i/(k-1)) for i in range(k)]
	
def dir_gen(k) :
	return npr.dirichlet((1, 1, 1), k) #equal weights mean symmetric?

def r2(A, W, z) :
	m = len(W[0]) #find neater more intuitive way ??
	if len(z) != m:
		raise ValueError("Args must have the same number of objective dimensions")
	
	sum = 0
	
	for w in W :
		min_ = []
		
		for a in A :
			if len(a) != m:
				raise ValueError("Args must have the same number of objective dimensions")
	
			max_ = [] 
			
			for j in range(m): 
				max_.append( w[ j ] * abs( z[ j ] - a[ j ] ))
			min_.append(max(max_))
		# add min of max to sum for each w in W	
		sum += min(min_)
	return sum/len(W) 
	

def r2_weights(A, W, z) :
	m = len(W[0]) #find neater more intuitive way ??
	if len(z) != m:
		raise ValueError("Args must have the same number of objective dimensions")
	
	sum = 0
	weights = dict.fromkeys(W)
	for w in W :
		min_ = []
		
		for a in A :
			if len(a) != m:
				raise ValueError("Args must have the same number of objective dimensions")
			max_ = [] 
			
			for j in range(m): 
				max_.append( w[ j ] * abs( z[ j ] - a[ j ] ))
			min_.append(max(max_))
		# add min of max to sum for each w in W	
		minimum = min(min_)
		i = min_.index(minimum)
		
		weights[w] = A[i]
		
		sum += min(min_)
	print(weights)
	return sum/len(W), weights
		
	
if __name__ == "__main__":
	A = [(0, 1), (0.33,0.18), (0.67, 0.03), (1, 0)]
	#A = weights_gen(11)
	W = weights_gen(10)
	#print(W)
	z = (0, 0)
	#for w in W:
	#	l = [(0, 0), w]		
	#	plt.plot(list(zip(*l)))	
	#	plt.show()
	#print(list(zip(*W)))
	
	#for w in W:
	#	plt.quiver(w[0], w[1], angles='xy', scale_units='xy', scale=21)
	#plt.xlim((0))
	#plt.ylim((0))
	#plt.show()
	
	r, weights = r2_weights(A, W, z)
	
	plt.axis('scaled')
	plt.xlim(-0.05, 1.05)
	plt.ylim(-0.05, 1.05)
	for value in weights.items():
		for w in W:
			w0, w1 = 2*w[0], 2*w[1]
			plt.plot((0, w0), (0, w1), linewidth=0.7, color='grey')
		#plt.scatter(value[0], value[1])
	
	plt.scatter(list(zip(*A))[0], list(zip(*A))[1])
	plt.show()
	
	
	print(weights)
	