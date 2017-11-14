# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 05:07:14 2017

@author: rohitt
"""



helper.py




# /usr/bin/env python3

import csv
import math

def getData(filename):
	filepath = "dataset/" + filename

	finalset = []

	with open(filepath, 'rt') as file:
		data = csv.reader(file)
		for row in data:
			currentrow = {}
			currentrow['user'] = int(row[0])
			currentrow['movie'] = int(row[1])
			currentrow['rating'] = float(row[2])
			finalset.append(currentrow)
	return finalset

def getUserData(userid, data):
	newdata = []
	for elem in data:
		if elem['user'] == userid:
			newdata.append(elem)
	return newdata

def rmserror(data1, data2):
	if not len(data1) == len(data2):
		raise ValueError('RMS Error called with lists of differing lengths')
	mean = 0
	for i in range(len(data1)):
		diff = data1[i] - data2[i]
		mean = mean + diff * diff
	mean = mean / len(data1)
	return math.sqrt(mean)

def precisionatk(predicted, data):
	newdata = []
	for i in range(len(predicted)):
		for j in range(len(data)):
			if predicted[i]['movie'] == data[j]['movie']:
				newrow = {}
				newrow['user'] = data[j]['user']
				newrow['movie'] = data[j]['movie']
				newrow['predicted'] = predicted[i]['rating']
				newrow['actual'] = data[j]['rating']
				newdata.append(newrow)
	relevant = []
	recommended = []
	for i in range(len(newdata)):
		if newdata[i]['actual'] >= 3.5:
			relevant.append(newdata[i])
		if newdata[i]['predicted'] >= 3.5:
			recommended.append(newdata[i])
	def sortrecommended(elem):
		return elem['predicted']
	list.sort(recommended, key=sortrecommended, reverse=True)
	recommended = recommended[:len(relevant)]
	commoncount = 0
	for i in range(len(relevant)):
		for j in range(len(recommended)):
			if relevant[i]['movie'] == recommended[j]['movie']:
				commoncount = commoncount + 1
	precision = (commoncount * 100) / len(recommended)
	rval = {}
	rval['precision'] = precision
	rval['k'] = len(recommended)
	return rval

def spearmanrank(data1, data2):
	newdata = []
	for i in range(len(data1)):
		for j in range(len(data2)):
			if data1[i]['movie'] == data2[j]['movie']:
				newrow = {}
				newrow['rating1'] = data1[i]['rating']
				newrow['rating2'] = data2[j]['rating']
				newdata.append(newrow)
	def sort1(elem):
		return elem['rating1']
	list.sort(newdata, key=sort1)
	for i in range(len(newdata)):
		newdata[i]['rank1'] = i
	def sort2(elem):
		return elem['rating2']
	list.sort(newdata, key=sort2)
	for i in range(len(newdata)):
		newdata[i]['rank2'] = i
	sumofdiffdiff = 0
	for i in range(len(newdata)):
		diff = newdata[i]['rank1'] - newdata[i]['rank2']
		sumofdiffdiff = sumofdiffdiff + diff * diff
	n = len(newdata)
	if n <= 1:
		rank = 1
	else:
		rank = 1 - (6 * sumofdiffdiff) / (n*(n*n - 1))
	rval = {}
	rval['count'] = n
	rval['rank'] = rank
	return rval

def pearson(data1, data2):
	newdata = []
	for i in range(len(data1)):
		for j in range(len(data2)):
			if data1[i]['movie'] == data2[j]['movie']:
				newrow = {}
				newrow['rating1'] = data1[i]['rating']
				newrow['rating2'] = data2[j]['rating']
				newdata.append(newrow)
	sumx=0
	sumy=0
	sumxy=0
	sumxx=0
	sumyy=0
	meanx=0
	meany=0
	for i in range(len(newdata)):
		sumx = sumx + newdata[i]['rating1']
		sumy = sumy + newdata[i]['rating2']
		sumxy = sumxy + newdata[i]['rating1'] * newdata[i]['rating2']
		sumxx = sumxx + newdata[i]['rating1'] * newdata[i]['rating1']
		sumyy = sumyy + newdata[i]['rating2'] * newdata[i]['rating2']
	n = len(newdata)
	if n <= 1:
		rank = 1
	else:
		meanx = sumx/n
		meany = sumy/n
		num = sumxy - n*meanx*meany
		den1 = math.sqrt(sumxx - n*meanx*meanx)
		den2 = math.sqrt(sumyy - n*meany*meany)
		if den1 * den2 ==0:
			rank = 0
		else:
			rank = (num) / (den1*den2)
	rval = {}
	rval['count'] = n
	rval['rank'] = rank
	return rval

def precisionAtRankK(mat, final, rank):
    count = 0.00
    match = 0.00
    for movie in rank:
        for user in mat[movie].keys():
            count = count+1
            a = (mat[movie][user])
            b = (final[movie][user])
            if (a == b):
                match = match+1
    precision = float((match*100))/count
    return precision

def spearman(mat, final):
    count = 0
    sumds = 0
    for movie in mat.keys():
        for user in mat[movie].keys():
            sumds = sumds + (float(mat[movie][user])-float(final[movie][user])) ** 2
            count = count + 1
            sumds = 6 * sumds
            den = (count ** 3) - count
    p = 1-(sumds/den)
    return p








collab.py







original = {}
matrix = {}
users = {}
complete = {}
test = {}

import re
import math
import heapq
import copy
import timeit
import helper

# Getting k nearest neighbours 
k = raw_input('Enter the number of items in the similarity set S: ')

###### Creating the ratings matrix #######

print('This may take some time...')

# Start time
start=timeit.default_timer()

# Opening file to read data
with open("ml-100k/u1.base") as f:
#with open("Aratings.txt") as f:
	for line in f:
		tokens = re.split("\t|\r|\n", line)
		#print(tokens)

		# Creating matrix/dictionary 
		if tokens[1] not in matrix.keys():
			matrix.update({tokens[1]: {tokens[0]: tokens[2]}})
			test.update({tokens[1]: {tokens[0]: tokens[2]}})
		else:
			matrix[tokens[1]].update({tokens[0]: tokens[2]})
			test[tokens[1]].update({tokens[0]: tokens[2]})

		# Creating a list of users IDs
		if tokens[0] not in users.keys():
			users.update({tokens[0]:[tokens[2]]})
		else:
			users[tokens[0]].append(tokens[2])

# Creating test matrix 
with open('ml-100k/u1.test') as f1:
#with open("Tratings.txt") as f1:
	for line in f1:
		tokens = re.split("\t|\r|\n", line)
		if tokens[1] in matrix.keys():
			if tokens[1] not in test.keys():
				test.update({tokens[1]: {tokens[0]: tokens[2]}})
			else:
				test[tokens[1]].update({tokens[0]: tokens[2]})

original = copy.deepcopy(matrix)

rating = 0
for movie in matrix.keys():
	n = len(matrix[movie])
	listen = 0
	for user in matrix[movie].keys():
		listen += int(matrix[movie][user])
	rating += listen
	mean = float(listen)/n
	for user in matrix[movie].keys():
		matrix[movie][user] = str(int(matrix[movie][user]) - mean)

# Global average ratings mu
mu = float(rating)/len(matrix)	

# Calculating magnitude of each movie vector
magnitude = {}
for movie in matrix.keys():
	value = 0
	for user in matrix[movie].keys():
		value += (float(matrix[movie][user]) ** 2)
	value = math.sqrt(value)
	magnitude.update({movie:str(value)})

###### Predict their ratings ######

for movieID in matrix.keys():
	similarity = {}
	for movie in matrix.keys():
		if movie == movieID:
			similarity.update({movieID: 1})
		else:
			value = 0
			for user in matrix[movie].keys():				
				if user in matrix[movieID].keys():
					value += (float(matrix[movie][user]) * float(matrix[movieID][user]))						
			if float(magnitude[movie]) == 0 or float(magnitude[movieID]) == 0:
				value = 0
			else:
				value = value / (float(magnitude[movie])*float(magnitude[movieID]))				
			similarity.update({movie: str(value)})


	# Get k most similar movies to movieID
	rank = heapq.nlargest(int(k), similarity, key=similarity.get)

	# For users who have not rated movieID, predict their ratings for movieID
	for userID in users.keys():
		# Baseline estimate: average rating of user x / userID 
		ratingsum = 0
		for i in range(len(users[userID])):
			ratingsum += int(users[userID][i])
		bx = float(ratingsum)/len(users[userID])

		if userID not in matrix[movieID].keys():
	
			# Weighted average
			n_val = 0
			d_val = 0
			for m in rank:
				# m is a movie from the k nearest neighbors of movieID

				ratsum = 0
				for j in original[m].keys():
					ratsum += int(original[m][j])

				bj = float(ratsum)/len(original[m])
				bxj = bx + bj - mu

				if userID in matrix[m].keys():
					# Pearson correlation similarity metric
					d_val += float(similarity[m])
					n_val += (float(similarity[m]) * (float(original[m][userID])) - bxj)
			if d_val == 0:
				# Places zero for every rating it cannot predict
				count = 0 
			else: 

				count = n_val/d_val
			
			ratsum = 0
			for i in original[movieID].keys():
				ratsum += int(original[movieID][i])
			bi = float(ratsum)/len(original[movieID])
			bxi = bx + bi - mu
			count += bxi

			if movieID not in complete.keys():
				complete.update({movieID: {userID: count}})
			else:
				complete[movieID].update({userID: count})

		else:
			# Add the known values to the new matrix 
			if movieID not in complete.keys():
				complete.update({movieID: {userID: original[movieID][userID]}})
			else:
				complete[movieID].update({userID: original[movieID][userID]})

# End time
print "\nTime taken for prediction:"
stop=timeit.default_timer()
print "%s seconds" %(stop-start)

###### Evaluating the errors between test (actual) and complete (predicted) ###### 

### RMSE ###
# rmse = errors.rmse_collab(test, complete)
# rmse = helper.rmserror(test,complete)
# print "\nThe RMSE error is: "
# print rmse

### Top k precision ###
ponker = helper.precisionAtRankK(test, complete, rank)
print "\nThe precision on top " + k +" is: "
print ponker

### Spearman coefficient ###
sp = helper.spearman(test, complete)
print "\nThe Spearman Rank correlation is: "
print sp






svd.py







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







cur.py







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







main.py






#CODE TO EXECUTE SVD AND CUR ON MOVIE RATINGS
k = input("Enter Dimensionality for SVD (Usually the number of users): ") 
k = int(k)
r = input("enter r i.e number of rows/columns to pick in CUR : ") #enter r
r = int(r)
import svd #opening svd.py
import cur #opening cur.py
import os #import os for file exist checks
import numpy as np #numpy import
import json #import json for dumping matrices
from pympler import asizeof #import pympler for space usage estimation
import sys #importing sys for y/n confirmation

directory='./reports'
if not os.path.exists(directory):
    os.makedirs(directory)
def query_yes_no(question, default="yes"): #y/n question class
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

svd_usage=asizeof.asizeof(svd) #calculate space usage for svd
cur_usage=asizeof.asizeof(cur) #calculate space usage for cur

class MyEncoder(json.JSONEncoder): #custom class to facilitate json serialization of numpy objects
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

print('Writing report') #processing done and started output
try:
    os.remove("./reports/report.txt") #delete files if they exist in order to prevent meaningless appends
except OSError:
    pass

try:
    os.remove("./reports/matrices.json")
except OSError:
    pass

report = open("./reports/report.txt", 'a') #open report file
string = """
******************************************************************
*  ASSIGNMENT - III                                              *
*  DATASET:   ml-latest-small FROM MovieLens                     *
*  USERS: 671                                                    *
*  MOVIES: 9000                                                  *
*  RATINGS: 100004                                                *
*  MEMBER 1: Aayush Barthwal 2015A7PS0136H                       *
*  MEMBER 2: Mukund Kothari 2015A7PS0133H                        *
*  MEMBER 3: Rohitashva Vashishtha 2015B4PS0546H                 *
*  MEMBER 4: Tushar Aggarwal 2015A7PS0047H                       *
******************************************************************""" 
report.write("\n%s\n" % string) #printing ascci-art
report.write("Time taken by SVD Algorithm: %f" % svd.svd_time)
report.write(" seconds\n")
report.write("Time taken by CUR Algorithm: %f" % cur.cur_time)
report.write(" seconds\n")
report.write("Space taken by SVD Algorithm: %d" % svd_usage)
report.write(" KB\n")
report.write("Space taken by CUR Algorithm: %d" % cur_usage)
report.write(" KB\n")
report.write("Frobenius error in SVD: ")
print(svd.frobenius_svd,file=report)
report.write("Frobenius error in CUR: ")
print(cur.frobenius_cur,file=report)
report.write("------------------------------------------------------------------\n")
report.write("COMPARISION\n")
if svd.svd_time < cur.cur_time:
	report.write("SVD is faster\n")
else:
	report.write("CUR is faster\n")
if svd_usage < cur_usage:
	report.write("SVD is more space efficient\n")
else:
	report.write("CUR is more space efficient\n")
if svd.frobenius_svd > cur.frobenius_cur:
	report.write("CUR is more accurate\n")
else:
	report.write("SVD is more accurate\n")
report.write("------------------------------------------------------------------\n")
report.write("U matrix in SVD\n") #printing all the matrices calculated in svd and cur
print(svd.U,file=report)
report.write("------------------------------------------------------------------\n")
report.write("V Transpose matrix in SVD\n")
print(svd.V_transpose,file=report)
report.write("------------------------------------------------------------------\n")
report.write("S matrix in SVD\n")
print(svd.S,file=report)
report.write("------------------------------------------------------------------\n")
report.write("Final matrix in SVD\n")
print(svd.M2,file=report)
report.write("------------------------------------------------------------------\n")
report.write("C matrix in CUR\n")
print(cur.C,file=report)
report.write("------------------------------------------------------------------\n")
report.write("U matrix in CUR\n")
print(cur.U,file=report)
report.write("------------------------------------------------------------------\n")
report.write("R matrix in CUR\n")
print(cur.R,file=report)
report.write("------------------------------------------------------------------\n")
report.write("Final matrix in CUR\n")
print(cur.CUR,file=report)


