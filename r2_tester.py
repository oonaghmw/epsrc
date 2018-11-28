import r2, nd, random, csv
import matplotlib.pyplot as plt
import numpy as np
"""
Run tests and graph results for the r2 function in 
the r2 module
"""

def weights_gen( k ) :
	"""
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
	
### TWO DIMENSIONAL ###
def generate_pareto( p, step ):
	"""
	add args to make customisable
	"""
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
	
def r2_plot( ps, r2s ): 
	r2plot, = plt.plot( ps, r2s ) # any point in the = ?
	plt.title( "r2 value against p" )
	plt.xlabel( "p value" )
	plt.ylabel( "r2" )
	plt.show()
	
def test_r2( W ):
	r2s = []
	rows = [["p", "r"]]
	ps  = np.arange( 0.1, 3.1, 0.2 )
	for p in ps:
		A = generate_pareto( p, 5 )		
		r = r2.r2( A, W, ( 0,0 ) )
		r2s.append( r) #r2.r2( A, W, ( 0,0 ) ) )
		
		rows.append([p, r])
		A_plot = plt.plot( list( zip(* A ) )[0], list( zip(* A ) )[1], label = round( p, 2 ) ) # any point in the = ?
		plt.legend( loc = 1, ncol = 2, fontsize = 7,  title = "value of p" )
	
	plt.title ( "Pareto Fronts" )
	plt.xlabel( "f2(x)" )
	plt.ylabel( "f1(x)" )
	
	plt.show() 
		
	r2_plot( ps, r2s ) 
	
	try:			
		data = open( "r2_data.csv", "w", newline = '' )
		with data:
			writer = csv.writer( data )
			writer.writerows( rows )
		data.close()
	except IOError:
		print( "Problem writing to file!" )
	
	return r2s

def test_weights():
	for w in range( 2, 10 ):
		W  = weights_gen( w )
		r2s = []
		ps  = np.arange( 0.1, 3.1, 0.2 )
		
		for p in ps:
			A  = generate_pareto( p, 5 )		
			r2s.append( r2.r2( A, W, ( 0,0 ) ) )
		plt.plot( ps, r2s, label = w )
		plt.legend( fontsize = 7, title = "no. weights" )#think of better title
		
	plt.title ( "r2 value against p" )
	plt.xlabel( "p value" )
	plt.ylabel( "r2" )
	plt.show()
	
def test_w(): 
	"""
	pointless, mostly just linear, stays the same for different w
	"""
	A = generate_pareto(4, 10)		
	r2s = []
	
	for w in np.arange(2, 10):
		W = weights_gen(w)
		r = r2.r2(A, W, (0,0))
		r2s.append(r)
		
			
	plt.plot(np.arange(2, 10), r2s)
	#plt.legend(fontsize = 7, title = "no. weights")#think of better title
		
	plt.title("r2 value for different number weights")
	plt.xlabel("weights")
	plt.ylabel("r2")
	plt.show()
	
def test_points():
	r2s    = []
	points = list( range( 1, 15 ) )
	W      = weights_gen( 5 )
	for point in points:
		A = generate_pareto( 1, point )
		r2s.append( r2.r2( A, W, ( 0, 0 ) ) )
	
		
	print( points, r2s )
	plt.plot( points, r2s )
	#plt.legend(fontsize = 7, title = "no. weights")#think of better title
		
	plt.title( "r2 value by number of points in A" )
	plt.xlabel( "Number points" )
	plt.ylabel( "r2" )
	plt.show()
		
if __name__ == "__main__":
	#W = weights_gen(3)
	#test_r2(W)
	pass