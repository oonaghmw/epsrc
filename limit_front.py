import r2, nd
import numpy as np
import matplotlib.pyplot as plt

W = r2.weights_gen(3)
z = (0, 0)

def limit_front(front, N):
	r2s = [r2.r2(front[:i] + front[i+1:], W, z) for i in range(len(front))]
	new_front = front.copy()
	
	for _ in range(len(front) - N):
		new_front.remove(front.pop(r2s.index(min(r2s))))
		r2s.remove(min(r2s))
	return new_front

"""
pass in a non dominated set only
"""
def remove_one(front):
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
	m = min(contribs, key=contribs.get)	
	front.remove(m)
	return front
	
def remove_many(front, N=1):
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
		m = min(contribs, key=contribs.get)	
		front.remove(m)
	return front	
	



#X = [tuple(np.random.rand(2)) for i in range(1000)]

#X = [(0, 6), (1, 5), (2, 1), (4, 6), (5, 1), (6.5, 4), (6, 0)]



#nd_X = [X[i] for i in nd.nondom(np.array(X))]
#print(nd_X)
#n = nd_X.copy()

#plt.scatter(list(zip(*nd_X))[0], list(zip(*nd_X))[1]) 
#L = remove_many(nd_X, 2)
#print(L, r2.r2(L, W, z))

#plt.scatter(list(zip(*n))[0], list(zip(*n))[1]) 
#plt.scatter(list(zip(*L))[0], list(zip(*L))[1], c='r', marker='.')
#plt.title("resulting front")
#plt.show()