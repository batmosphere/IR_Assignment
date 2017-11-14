# User-movie rating matrix
original = {}
matrix = {}
users = {}
complete = {}
test = {}

# Importing libraries
import re
import math
import heapq
import copy
import timeit
# import errors
import helper

# Getting k nearest neighbours 
k = raw_input('Enter the number of items needed in the similarity set S: ')

###### Creating the ratings matrix #######

print('This may take a few minutes...')

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

#print('Matrix')
#print(matrix)
#print('Users matrix')
#print(users)

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
#print(test)

# Make a copy of the matrix 
original = copy.deepcopy(matrix)

# Calculating mean rating of each movie and nornmalising the movie vector 
# Now matrix wil contain rating deviation of each movie 
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
#print('Normalised Matrix')
#print(matrix)

# Calculating magnitude of each movie vector
magnitude = {}
for movie in matrix.keys():
	value = 0
	for user in matrix[movie].keys():
		value += (float(matrix[movie][user]) ** 2)
	value = math.sqrt(value)
	magnitude.update({movie:str(value)})
#print('Magnitude')
#print(magnitude)

###### For each movie find out the users who have not rated the movie ######
###### Predict their ratings ######

for movieID in matrix.keys():
	# Similarity calculation between the current movie and remaining other movies 
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
	#print('Similarity of movie '+movieID)
	#print(similarity)

	# Get k most similar movies to movieID
	rank = heapq.nlargest(int(k), similarity, key=similarity.get)
	#print(rank)

	# For users who have not rated movieID, predict their ratings for movieID
	for userID in users.keys():
		# Baseline estimate: average rating of user x / userID 
		ratingsum = 0
		for i in range(len(users[userID])):
			ratingsum += int(users[userID][i])
		bx = float(ratingsum)/len(users[userID])

		if userID not in matrix[movieID].keys():
			# Now we have movieID and userID	
			# Time to predict the unknown values!
			# Weighted average
			n_val = 0
			d_val = 0
			for m in rank:
				# m is a movie from the k nearest neighbors of movieID

				# Calculate baseline bxj / average ratings for movie m
				ratsum = 0
				for j in original[m].keys():
					ratsum += int(original[m][j])

				bj = float(ratsum)/len(original[m])
				bxj = bx + bj - mu

				# Calculate similarity if userID has rated movie m 
				if userID in matrix[m].keys():
					# Calculating the denominator and numerator values for the 
					# Pearson correlation similarity metric
					d_val += float(similarity[m])
					n_val += (float(similarity[m]) * (float(original[m][userID])) - bxj)
			if d_val == 0:
				# Places zero for every rating it cannot predict
				count = 0 
				#print("Can't calculate count for user "+userID+' for movie '+movieID)
			else: 
				# Unknown rating is the weighted average of the known ratings with similarities between 
				# the k most similar movies 
				count = n_val/d_val
				#print('The listen count for user '+userID+' for movie '+movieID+' is '+str(count))
			
			# Calculate baseline bxi / average ratings for movie movieID
			ratsum = 0
			for i in original[movieID].keys():
				ratsum += int(original[movieID][i])
			bi = float(ratsum)/len(original[movieID])
			bxi = bx + bi - mu
			count += bxi

			# Add the predicted values to the new matrix
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

#print('Complete matrix')
#print(complete)

#print('Test matrix')
#print(test)

# End time
print "\nTime taken for prediction:"
stop=timeit.default_timer()
print "%s seconds" %(stop-start)

###### Evaluating the errors between test (actual) and complete (predicted) ###### 

### RMSE ###
# rmse = errors.rmse_collab(test, complete)
# rmse = helper.rmserror(test,complete)
print "\nThe RMSE error is: "
print rmse

### Top k precision ###
ponk = helper.ponk_collab(test, complete, rank)
print "\nThe precision on top " + ponk['k'] +" is: "
print ponk

### Spearman coefficient ###
srcr = helper.srcr_collab(test, complete)
print "\nThe Spearman Rank correlation is: "
print srcr

