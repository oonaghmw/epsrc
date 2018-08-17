import r2, nd
import numpy as np
import matplotlib.pyplot as plt
import r2_evo as r2e
import random
import time 

"""
Iteratively calculates point in front which removing will contribute 
least to the R2 value of the front, then removes it. This is done until
desired number of points are removed from front.
Quite a slow process but generally results in better front than 
remove_many_one.
Args: 
	front	- list of tuples representing the coordinates for a NON DOMINATED front
	W		- List of weight vectors as tuples to calculate R2 with
	z		- tuple representing utopian point to calculate R2 with
	N		- number of points to remove. 
Returns:
	list of tuples representing points remaining in the truncated front.
Warnings:
	Most effective when front is already non dominated.
"""	
def remove_many_it(front, W, z, N=1):
	if len(front) <= N:
		raise ValueError("Trying to remove more points than are available")
	for _ in range(N):
		base_r2 = r2.r2(front, W, z)
	
		contribs = {}
		for p in front:
			front_ = front.copy()
			front_.remove(p)
		
			r = r2.r2(front_, W, z)
			contr = abs(base_r2 - r)
		
			contribs[p] = contr
		front.remove(min(contribs, key=contribs.get))
	return front

"""
Calculates points in front which removing will contribute 
least to the R2 value of the front, orders them with increasing
contribution then removes N of the first points in the order in one go.
Faster algorithm than remove_many_it but generally results in front
with worse R2 value. 
Args: 
	front	- list of tuples representing the coordinates for a NON DOMINATED front
	W		- list of weight vectors as tuples to calculate R2 with
	z		- tuple representing utopian point to calculate R2 with
	N		- number of points to remove. 
Returns:
	list of tuples representing points remaining in the truncated front.
Warnings:
	Most effective when front is already non dominated.
"""	
def remove_many_one(front, W, z, N=1):
	if len(front) <= N:
		raise ValueError("Trying to remove more points than are available")

	base_r2 = r2.r2(front, W, z)

	contribs = {}
	for p in front:
		front_ = front.copy()
		front_.remove(p)
	
		r = r2.r2(front_, W, z)
		contr = abs(base_r2 - r)
		
		contribs[p] = contr
		
	sorted_keys = sorted(contribs, key=contribs.__getitem__)
	for i in range(N):
		front.remove(sorted_keys[i])
	return front

"""
Equivalent behaviour to remove_many_it but displays graphs of the 
progress of the front. 
Args: 
	front	- list of tuples representing the coordinates for a NON DOMINATED front
	W		- list of weight vectors as tuples to calculate R2 with
	z		- tuple representing utopian point to calculate R2 with
	N		- number of points to remove. 
Returns:
	list of tuples representing points remaining in the truncated front.
Warnings:
	Most effective when front is already non dominated.
"""
def remove_many_graphic(front, W, z, N=1):
	if len(front) <= N:
		raise ValueError("Trying to remove more points than are available")
	for _ in range(N):
		base_r2 = r2.r2(front, W, z)

		print("base r2: ", base_r2)
		plt.scatter(list(zip(*front))[0], list(zip(*front))[1]) 
		plt.show()

		contribs = {}
		for p in front:
			front_ = front.copy()
			front_.remove(p)

			r = r2.r2(front_, W, z)
			contr = abs(base_r2 - r)

			print("Without ", p, "R2: ", r)
			print(p, "Contribution: ", contr)
			plt.scatter(list(zip(*front_))[0], list(zip(*front_))[1]) 
			plt.title("Front without %s" %(p,))
			plt.show()

			contribs[p] = contr
		front.remove(min(contribs, key=contribs.get))
	return front
	
	
"""
Evolutionary algorithm which, given an initial Pareto front, uses the R2 indicator 
defined in the r2 module to evolve a better performing front, ensuring the number of
points in the front is never above a given value. Utilises nondom function from nd and 
mutate function from r2_evo. 
Args:
	X 	 - initial set of points, a list of tuples giving the coordinates.
	W 	 - weight vector required for R2. A list of tuples.
	z 	 - utopian point, tuple giving coordinates.
	rate - number giving rate of mutation
	gens - number of iterations to run algorithm for.
	size - maximum size for list of points in the front.
Returna:
	dict - resulting Pareto front, dictionary with keys as points in the 
		   objective space, and values as their equivalent points in 
		   decision space. 
	r	 - value of r2 for the resulting Pareto front
"""
def trunc_evo( X, f, W, z, rate, gens, size):
	dict = { f(x): x for x in X }
	dict = r2e.dict_nondom(dict)

	if len(dict.keys()) > size: #this part takes a long time
		trunc = remove_many(list(dict.keys()), W, z, len(dict.keys())-size)
		dict = {t : dict[t] for t in trunc}

	r   = r2.r2( dict.keys(), W, z )
	r2s = [(0, r)]

	for i in range( gens ):
		a = random.choice( list(dict.keys()) ) 
		x = dict[a]
		x = r2e.mutate( x, rate ) 

		dict[f(x)] = x
		dict = r2e.dict_nondom(dict) #???
		
		if len(dict.keys()) > size:
			trunc = remove_many(list(dict.keys()), W, z, len(dict.keys())-size)
			dict = {t : dict[t] for t in trunc}
		r_	= r2.r2( dict.keys(), W, z )
		r = r_
		r2s.append((i+1, r))

	return dict, r

	
"""
Same behaviour as trunc_evo, but displays plot of progress of R2 value.
Args:
	X 	 - initial set of points, a list of tuples giving the coordinates.
	W 	 - weight vector required for R2. A list of tuples.
	z 	 - utopian point, tuple giving coordinates.
	rate - number giving rate of mutation
	gens - number of iterations to run algorithm for.
	size - maximum size for list of points in the front.
Returns:
	dict - resulting Pareto front, dictionary with keys as points in the 
		   objective space, and values as their equivalent points in 
		   decision space. 
	r	 - value of r2 for the resulting Pareto front
"""
def trunc_evo_graphic( X, f, W, z, rate, gens, size):
	dict = { f(x): x for x in X }
	dict = r2e.dict_nondom(dict)
	plt.scatter(list(zip(*dict))[0], list(zip(*dict))[1])
	plt.show()

	if len(dict.keys()) > size: #this part takes a long time
		trunc = remove_many_it(list(dict.keys()), W, z, len(dict.keys())-size)
		dict = {t : dict[t] for t in trunc}

	r   = r2.r2( dict.keys(), W, z )
	r2s = [(0, r)]

	for i in range( gens ):
		a = random.choice( list(dict.keys()) ) 
		x = dict[a]
		x = r2e.mutate( x, rate ) 

		dict[f(x)] = x
		dict = r2e.dict_nondom(dict) #???

		if len(dict.keys()) > size:
			trunc = remove_many_it(list(dict.keys()), W, z, len(dict.keys())-size)
			dict = {t : dict[t] for t in trunc}

		r_	= r2.r2( dict.keys(), W, z )

		r = r_
		r2s.append((i+1, r))

	plt.plot(list(zip(*r2s))[0], list(zip(*r2s))[1])
	plt.title("R2 value of front over generations")
	plt.xlabel("generation")
	plt.ylabel("R2 value")
	plt.show()
	return dict, r

"""
Similar to trunc_evo, but chooses random points to remove. Written to compare outcomes.
Does not converge to a low R2 value and R2 is liable to increase.
Args:
	X 	 - initial set of points, a list of tuples giving the coordinates.
	W 	 - weight vector required for R2. A list of tuples.
	z 	 - utopian point, tuple giving coordinates.
	rate - number giving rate of mutation
	gens - number of iterations to run algorithm for.
	size - maximum size for list of points in the front.
Returns:
	dict - resulting Pareto front, dictionary with keys as points in the 
		   objective space, and values as their equivalent points in 
		   decision space. 
	r	 - value of r2 for the resulting Pareto front
"""
def trunc_evo_rand( X, f, W, z, rate, gens, size):
	dict = { f(x): x for x in X }
	dict = r2e.dict_nondom(dict)
	plt.scatter(list(zip(*dict))[0], list(zip(*dict))[1])
	plt.show()

	if len(dict.keys()) > size:
		for _ in range(len(dict.keys())-size):
			dict.pop(random.choice(list(dict.keys())))
		plt.scatter(list(zip(*dict))[0], list(zip(*dict))[1])
		plt.show()



	r   = r2.r2( dict.keys(), W, z )
	r2s = [(0, r)]

	for i in range( gens ):
		a = random.choice( list(dict.keys()) ) 
		x = dict[a]
		x = r2e.mutate( x, rate ) 

		dict[f(x)] = x
		dict = r2e.dict_nondom(dict) #???

		if len(dict.keys()) > size:
			for _ in range(len(dict.keys())-size):
				dict.pop(random.choice(list(dict.keys())))


		r	= r2.r2( dict.keys(), W, z )
		r2s.append((i+1, r))

	plt.plot(list(zip(*r2s))[0], list(zip(*r2s))[1])
	plt.title("R2 value of front over generations")
	plt.xlabel("generation")
	plt.ylabel("R2 value")
	plt.show()
	return dict, r


if __name__ == "__main__":
	X = [(0, 0), (0.3, 0.3), (1, 1), (1, 0), (0, 1)]
	W = r2.weights_gen(10)
	z = (0, 0)

	print( remove_many_it(X, W, z))