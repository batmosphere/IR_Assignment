from __main__ import * #accesing variables from main
import numpy as np #numpy import
import math #for sqrt
import time #importing time to measure performance
from numpy import linalg as LA #scipy imports
from numpy.random import choice
np.set_printoptions(suppress=True)
np.random.seed(4896) #set constant seed

# 100004 ratings (1-5) from 671 users on 9000 movies. 
# Each user has rated at least 20 movies.
# replaced regex [,][^,]+\n with \n to remove timestamp
start_time = time.clock() 
m = 671 #users
n = 9125 #movies
N = 100004 #reviews
M = np.zeros((m, n)) #initialize rating matrix
M = np.matrix(M)

movies = [] #init arrays for storing users,movies and ratings
m2 = []
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

# r = input("enter r: ") #code to execute without main by asking user input
# r = int(r)


f = LA.norm(M)**2 #starting cur
colProbDist = [(LA.norm(M[:,x])**2)/f for x in range(n)]
rowProbDist = [(LA.norm(M[x])**2)/f for x in range(m)]
rand_cols = np.random.choice(range(n),r,False,colProbDist)
rand_rows = np.random.choice(range(m),r,False,rowProbDist)

C = np.matrix(np.zeros((m, r)))
R = np.matrix(np.zeros((r, n)))
W = np.matrix(np.zeros((r, r)))
for i in range(r):
	C[:,i] = M[:,rand_cols[i]]/math.sqrt(r*colProbDist[rand_cols[i]])
	R[i] = M[rand_rows[i]]/math.sqrt(r*rowProbDist[rand_rows[i]])

for i in range(r):
	for j in range(r):
		W[i,j] = M[rand_rows[i],rand_cols[j]]

# print C,R
X, Sig, Yt = LA.svd(W, full_matrices=False)
Sig = np.around(Sig, decimals=4)
i = 0
for x in Sig:
	if x != 0:
		Sig[i] = 1/x
	else:
		Sig[i] = 0
	i += 1
Sig = np.matrix(np.diag(Sig))

U = Yt.transpose()*Sig*Sig*X.transpose()
CUR = C*U*R;
frobenius_cur=LA.norm(abs(CUR)-M)
cur_time = time.clock() - start_time #stop runtime clokc
# print (CUR)