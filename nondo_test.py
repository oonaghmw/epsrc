import numpy as np
import nd
import matplotlib.pyplot as plt

#nondom tests

# no member of nondom set should be dominated by original set

X = [tuple(np.random.rand(2)) for i in range(6)]

plt.scatter(list(zip(*X))[0], list(zip(*X))[1]) 

nd_X = [X[i] for i in nd.nondom(np.array(X))]
plt.scatter(list(zip(*nd_X))[0], list(zip(*nd_X))[1], c='r')
plt.show()

def check_nondom(point, set):
	"""
	check that point is not dominated by ANY p in set.
	If point is dominated by any p in set then return False.
	"""
	for p in set:
		if all([i == j for i, j in zip(point, p)]) == True:
			pass
		else: #else redundant here
			if not any([i < j for i, j in zip(point, p) ]):
				return False
		
	return True
	
print(check_nondom((1, 0), [(1, 0), (1, 0), (100, 100)]))

print(nd_X)
for i in range(len(nd_X)):
	#print(X[i], X[:i] + X[i+1:])
	print(check_nondom(nd_X[i], X)) #nd_X[:i] + nd_X[i+1:]))