import numpy.random as nr
import numpy.linalg as nl
import dirichlet
from pylab import *

#==============================================================================

class DTLZ:

	def __init__(self, M):
		self.M = M;
		self.lowerLimit = zeros(self.parameters());
		self.upperLimit = ones(self.parameters());
		
	def validParameters(self, x):
		return all(x >= self.lowerLimit) & all(x <= self.upperLimit);
		
	def g1(self, x, m):
		"""
		The first constraint function from the DTLZ test problem suite.
		"""
		xm = x[m-1:];
		z = xm - 0.5;
		r = dot(z,z) - cos(20 * pi * z).sum();
		result = 100 * (xm.shape[0] + r);
		return result;
		
	def parameters(self):
		return 10 + (self.M-1);		
		
	def distanceToFront(self, x):
		return None;	

#-------------------------------------------------------------------------------

class DTLZ1(DTLZ):
	
	def __init__(self, M=3):
		DTLZ.__init__(self, M);
		self.M = M;
		
	def evaluate(self, x):
		"""
		DTLZ test problem 1.
		"""
		# Initialise the value of g(x) + 1, and an empty array to hold the results.
		gp1 = self.g1(x, self.M) + 1;
		f = zeros(self.M);
		
		f[0] = 0.5 * prod(x[0:self.M-1]) * gp1;
		for i in range(1, self.M-1):
			f[i] = 0.5 * prod(x[0:self.M-i-1]) * (1 - x[self.M-i-1]) * gp1;
		f[self.M-1] = 0.5 * (1 - x[0]) * gp1;
		return f;
		
	def sample(self, N, M):
		X = dirichlet.randDirichlet(ones(M), 1000*M) / 2;
		return None, X;
		
	def toString(self):
		return "DTLZ1";

#-------------------------------------------------------------------------------

class DTLZ2(DTLZ):
	
	def __init__(self, M=3):
		DTLZ.__init__(self, M);

	def evaluate(self, x):
		"""
		DTLZ test problem 2.
		"""
		return self.problem2(self.g2(x[self.M-1:]) + 1, x);
		
	def problem2(self, gp1, x):
		"""
		Problem 2 from the DTLZ test problem suite, used by problems 2, 3 and 4.
		"""
		f = zeros(self.M);
		
		for i in range(self.M):
			f[i] = gp1;
			if self.M-i-1 > 0:
				for j in range(self.M-1-i):
					f[i] *= cos((pi * x[j]) / 2);
			if i > 0:
				f[i] *= sin((pi * x[self.M-1-i]) / 2);
		return f;

	def g2(self, xm):
		"""
		The second constraint function from the DTLZ test problem suite.
		"""
		z = xm - 0.5;
		return pow(z,2).sum();		

	def sample(self, n, m):
		X = zeros((1000*m, m));
		for i in range(X.shape[0]):
			x=rand(m)
			X[i,:]=abs(x/nl.norm(x))
		return None, X;
	
	def toString(self):
		return "DTLZ2";
		
	def distanceToFront(self, x):
		return sqrt(dot(x, x))-1;
		
#-------------------------------------------------------------------------------

class DTLZ3(DTLZ2):

	def __init__(self, M=3):
		DTLZ2.__init__(self, M);
		
	def evaluate(self, x):
		return self.problem2(self.g1(x, self.M) + 1, x);
		
	def toString(self):
		return "DTLZ3";
	
#-------------------------------------------------------------------------------

class DTLZ4(DTLZ2):

	def __init__(self, M=3, alpha=100):
		DTLZ2.__init__(self);
		self.M = M;
		self.alpha = alpha;
		
	def toString(self):
		return "DTLZ4";	
		
	#def evaluate(self, x):
	#	return self.problem2(self.g2(x[self.M:]) + 1, pow(x,self.alpha));			
		
	def evaluate(self, x):
		l = x.shape[0];
		objectives = zeros(self.M);
		
		# Calculate gxM.
		gxM = 0;		
		for i in range(self.M, l):
			gxM += gxM + pow(x[i] - 0.5, 2);
		gxM += 1;
		
		# Calculate fitness.
		objectives[0] = gxM;
		for i in range(self.M-1):
			objectives[0] = objectives[0] * cos(pow(x[i], self.alpha) * pi/2);
			
		for i in range(1, self.M):
			objectives[i] = gxM;
			j = 0;
			while j < (self.M-i-1):
				objectives[i] = objectives[i] * cos(pow(x[j], self.alpha) * pi / 2);
				j += 1;
				
			objectives[i] = objectives[i] * sin(pow(x[j], self.alpha) * pi / 2);
		return objectives;
		
"""
l=length(S);
objectives=zeros(1,m);
%calculate gxM
gxM=0;
for i=m:l;
  gxM=gxM+(S(i)-0.5)^2;
end
gxM=1+gxM;
%calculate fitness - contained in first elements of S (alongside gxM)
objectives(1)=gxM;
for i=1:m-1;
    objectives(1)=objectives(1)*cos((S(i)^alpha)*pi/2);
end
for i=2:m;
  objectives(i)=gxM;
  j=1;
  while(j<=m-i)
      objectives(i)=objectives(i)*cos((S(j)^alpha)*pi/2);
      j=j+1;
  end
  objectives(i)=objectives(i)*sin((S(j)^alpha)*pi/2);
end
"""


#-------------------------------------------------------------------------------	

class DTLZ5(DTLZ2):
	
	def __init__(self):
		self.M = 3;
		
	def evaluate(x):
		raise RuntimeError("This class has not been implemented yet");
		
	def toString(self):
		return "DTLZ5";
	
#-------------------------------------------------------------------------------

class DTLZ6(DTLZ):
	"""
	An implementation of DTLZ test problem 6. The problem has 2^{M-1} disconnected
	fronts, and has n = k + M - 1 decision variables, where k = 20.
	
	NB - in the original technical report, this is DTLZ7.
	"""
	
	def __init__(self, M=3):
		DTLZ.__init__(self, M=M);
		self.M = M;
		self.k = 20;
		
	def parameters(self):
		return self.M + 19;
		
	def evaluate(self, x):
		f = zeros(self.M);
		for i in range(self.M-1):
			f[i] = x[i];
			
		f[self.M-1] = (1 + self.g6(x)) * self.h(f, self.g6(x));
		return f;
			
	def g6(self, x):
		"""
		The constraint function for DTLZ6.
		"""
		xm = x[self.M-1:];
		return 1 + ((float(9) / xm.shape[0]) * xm.sum());			
		
	def h(self, f, g):
		fSum = 0;
		for i in range(self.M-1):
			fSum += (float(f[i]) / (1+g)) * (1 + sin(3 * pi * f[i]));
		return self.M - fSum;
		
	def toString(self):
		return "DTLZ6";

#-------------------------------------------------------------------------------
	
#-------------------------------------------------------------------------------

#def g1(x, m):
#	"""
#	The first constraint function from the DTLZ test problem suite.
#	"""
#	xm = x[m-1:];
#	z = xm - 0.5;
#	r = dot(z,z) - cos(20 * pi * z).sum();
#	result = 100 * (xm.shape[0] + r);   
#	return result;
	
##-------------------------------------------------------------------------------

#d#ef g2(xm):
#	"""
#	The second constraint function from the DTLZ test problem suite.
#	"""
#	z = xm - 0.5;
#	return pow(z,2).sum();

#-------------------------------------------------------------------------------

#d#ef g6(xm):
#	"""
#	The constraint function for DTLZ6.
#	"""
#	return 1 + (9 / xm.shape[0]) * sum(xm);
#
##-------------------------------------------------------------------------------
#
#def h6(f, g, M):
#	"""
#	The second constraint function for DTLZ6.
#	"""
#	s = 0;
#	for i in range(M-1):
#		s += ((f[i] / (1 + g)) * (1 + sin(3 * pi * f[i])));
#	return M - s;
#	
##-------------------------------------------------------------------------------

#def dtlzConstraints(x):
#	"""
#	Returns true if the decision variable meets the constraints for the DTLZ test
#	problem suite (ie, all x are in [0, 1]).
#	"""
#	return all(x < 1) & all(x > 0);
#	
##-------------------------------------------------------------------------------
#
#def sampleDtlz(P, N, M=3, problem=dtlz1):
#	X = rand(P, M - 1);
#	Y = zeros((P, N - (M - 1)));
#	if (problem == dtlz6) == False:
#		for i in range(P):
#			for j in range(N - (M - 1)):
#				Y[i,j] = 0.5;
#	Z = concatenate((X, Y), axis=1);
#	
#	A = zeros((P, M));
#	for i in range(P):
#		A[i,:] = problem(Z[i,:], M=M);
#	return A;
#	
#-------------------------------------------------------------------------------
