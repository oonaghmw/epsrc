import r2, nd, r2_evo, random
import matplotlib.pyplot as plt
import numpy as np

"""
#for p in np.arange(0.2, 2.2, 0.2):
#	x1 = np.linspace(0, 1, 5)
#	x2 = (1-x1**p)**(1/p)
	#set w
	
	#plt.scatter(x1, x2)
	#plt.grid(True)
	#plt.xlabel("f1(x)")
	#plt.ylabel("f2(x)")
	#plt.title(" A for when p = {}".format(p))
	#plt.show()
	
	#A = list(zip(x1, x2))
	#r_2 = r2.r2(A, W, z)
	#r2s.append(r_2)
	#with open("test.txt", "a") as txtfile:
	#	txtfile.write("\np = %s\nA = %s\nr2 = %s" % (p, A, r_2))
"""	

	try:			
		data = open("test_data.csv","w+", newline='')
		with data:
			writer = csv.writer(data)
			writer.writerows(test_data)
		data.close()
	except IOError:
		print("Problem writing to file!")
