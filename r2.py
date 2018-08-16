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
"""

def generate_pareto( p, step ):
	x1 = np.linspace( 0, 1, step )
	x2 = ( 1 - x1**p ) ** ( 1/p )
	return list( zip( x1, x2 ) )
	
def graph_front( front, p ):
	plt.scatter( list( zip(* front ) )[0], list( zip(* front ) )[1] )
	plt.grid( True )
	plt.xlabel( "f1(x)" )
	plt.ylabel( "f2(x)" )
	plt.title( "A for when p = {}".format( p ) )
	plt.show()
	
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
def weights_gen(k) :
	return [(i/(k-1), 1-i/(k-1)) for i in range(k)]
	
def dir_gen(k) :
	return npr.dirichlet((1, 1, 1), k) #should 1 be different?

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
	
	
def r2_3(A, W, z) : #wrong, dumb , obselite
	m = len(W[0]) #find neater more intuitive way ??
	m = 3
	sum = 0
	
	for w in W :
		min_ = []
		
		for a in A :
			# print('\na in A: ', a )
			# list of _max for each a in A
			# min_.append(max( [ W[ j ] * abs( z[ j ] - a[ j ] ) for j in range( m ) ]))
			max_ = [] 
			
			for j in range(m): 
				max_.append( w[ j ] * abs( z[ j ] - a[ j ] ))
				#print('max: ', max_)	
			min_.append(max(max_))
			#print('new min: ', min_)
		# add min of max to sum for each w in W	
		sum += min(min_)
		#print('sum: ', sum)
	return sum/m 
	
if __name__ == "__main__":
	A = [(1, 0, 1), (0, 1, 0), (0, 0, 1)]
	W = dir_gen(3)
	#print(W)
	z = (0, 0, 0)
	
	r = r2(A, W, z)
	print(r)
	