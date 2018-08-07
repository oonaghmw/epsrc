import numpy.random as npr
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

def weights_gen(k) :
	weights = [(i/(k-1), 1-i/(k-1)) for i in range(k)]
	return weights #condense further?
	
def dir_gen(k) :
	return npr.dirichlet((1, 1, 1), k) #should 1 be different?

def r2(A, W, z) :
	m = len(W[0]) #find neater more intuitive way ??
	sum = 0
	
	for w in W :
		min_ = []
		
		for a in A :
			# list of _max for each a in A
			max_ = [] 
			
			for j in range(m): 
				max_.append( w[ j ] * abs( z[ j ] - a[ j ] ))
			min_.append(max(max_))
		# add min of max to sum for each w in W	
		sum += min(min_)
	return sum/len(W)#/m 
	
	
def r2_3(A, W, z) :
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
	A = [(1, 0, 1), (1, 1, 0), (0, 0, 1)]
	W = dir_gen(3)
	print(W)
	z = (0, 0, 0)
	
	r = r2_3(A, W, z)
	print(r)