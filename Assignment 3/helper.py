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