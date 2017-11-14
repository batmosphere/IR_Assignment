from __main__ import * #accesing variables from main
import numpy as np #numpy import
from scipy import linalg #scipy imports
import scipy.sparse.linalg as la
from numpy.linalg import matrix_rank
from numpy import linalg as LA
from numpy.linalg import inv
import time #importing time to measure performance
# 100004 ratings (1-5) from 671 users on 9000 movies. 
# Each user has rated at least 20 movies.
# replaced regex [,][^,]+\n with \n to remove timestamp 
start_time = time.clock() #starting runtime clock
m = 671 #users
n = 9125 #movies
N = 100004 #reviews
M = np.zeros((m, n)) #initialize rating matrix
M = np.matrix(M)
k=0;
# if(len(sys.argv) > 1): #code to execute without main by giving dimension as command line argument
# 	k = int(sys.argv[1])

movies = [] #init arrays for storing users,movies and ratings
m2 = []
users = []
ratings = []
f = open("./ratings.csv", 'r') #opening dataset
next(f) #skipping first line
for line in f: #csv parsing
	temp = line.split(",")
	i = int(temp[0])-1
	users.append(i)
	j = int(temp[1])-1
	movies.append(j)
	m2.append(j)
	rating = float(temp[2])
	ratings.append(rating)
# 	 M[i,j] = rating
f.close
mapped_mat = [] #mapping movies spread over large range of numbers to reduce sparsity
m2 = np.unique(m2)
for i in range(164980):
	mapped_mat.append(0)
for i in range(len(m2)):
	mapped_mat[m2[i]] = i;
f = open("ratings.csv", 'r')
next(f)
for line in f:
	temp = line.split(",")
	i = int(temp[0])-1
	j = int(temp[1])-1
	rating = float(temp[2])
	M[i,mapped_mat[j]] = rating



r = matrix_rank(M) #starting svd
def svd(M, k=r):
	MT = M.transpose()
	MMT = M*MT
	MTM = MT*M
	if m < n:
		if k < min(m,n):
			s,U = la.eigsh(MMT,k)
		else:
			s,U = LA.eigh(MMT)
		U = np.fliplr(U)
		s = np.flipud(s)
		s = np.sqrt(s)
		S = np.diag(s)
		Vt = np.dot(np.dot(inv(S), U.transpose() ), M)
	else:
		if k < min(m,n):
			s,V = la.eigsh(MTM,k) #calculating eigen values and vectors
		else:
			s,V = LA.eigh(MTM)
		V = np.fliplr(V)
		s = np.flipud(s)
		s = np.sqrt(s)
		S = np.diag(s)
		U = M * V * inv(S)
		Vt = V.transpose
	return np.matrix(U),np.matrix(Vt),np.matrix(S),s
# print ('computing svd ')
for i in range(r,r-10,-1):
	U,V_transpose,S,s = svd(M,i)
	M2 = U*S*V_transpose #final matrix
svd_time=time.clock() - start_time #stop runtime clock
frobenius_svd=LA.norm(abs(M2)-M) #calculate error

# print ('computing inbuilt svd') #code to check with inbuilt svd function
# U3, S3, V3 = linalg.svd(M, full_matrices=False)
# S3_diag = np.diag(S3)
# M3 = np.matrix(U3)*np.matrix(S3_diag)*np.matrix(V3)
# print (LA.norm(abs(M3)-M))

