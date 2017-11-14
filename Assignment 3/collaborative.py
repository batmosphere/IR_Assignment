# /usr/bin/env python3

# Implement the collaborative recommendation

import helper

def filter(userdata, data):
	similarity = []
	for i in range(600):
		elem = helper.getUserData(i+1, data)
		rankdata = helper.pearson(userdata, elem)
		rankdata['user'] = i+1
		similarity.append(rankdata)
	def sort(elem):
		return elem['rank']
	list.sort(similarity, key=sort, reverse=True)
	# for each in similarity:
		# print(each)
	bymovie = []
	for row in data:
		num = 0
		den = 0
		flag = True
		index = None
		for eachvalue in userdata:
			if eachvalue['movie'] == row['movie']:
				flag = False
		if flag:
			for i in range(len(bymovie)):
				if bymovie[i]['movie'] == row['movie']:
					num = bymovie[i]['num']
					den = bymovie[i]['den']
					index = i
					# print("Found")
			# print(len(similarity))
			for eachsim in similarity:
				rating = row['rating']
				# print(rating)
				similarityval = eachsim['rank']
				num = num + similarityval * rating;
				den = den + similarityval;
				if index:
					bymovie[index]['num'] = num
					bymovie[index]['den'] = den
					# print("Updating")
				else:
					newval = {}
					newval['movie'] = row['movie']
					newval['num'] = num
					newval['den'] = den
					bymovie.append(newval)
					# print("Appending")
					# print(len(bymovie))
	for i in range(len(bymovie)):
		bymovie[i]['rating'] = bymovie[i]['num']/bymovie[i]['den']
	return bymovie
