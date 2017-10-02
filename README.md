# Search Engine Using Inverted Index

This project has been written as the CS F469 Informaton Retrieval Assignment 1. The project implements a basic search engine in Python using Inverted Index to query from the Brown Corpus. We could theoretically expand the codebase to search through any similar database with relative ease.

## Team

1. **Aayush Barthwal** - 2015A7PS0136H
2. **Mukund Kothari** - 2015A7PS0133H
3. **Rohitt Vashishtha** - 2015B4PS0546H
4. **Tushar Aggarwal** - 2015A7PS0047H

## Setting Up

1. First, clone the project from git using `git clone https://github.com/batmosphere/IR_Assignment`.
2. Set up a virtual env (optional) for better namespacing.
3. Run `sudo apt install python3-tk portaudio19-dev python3-all-dev` to install system wide dependencies.
4. Run `pip install -r requirements.txt` to install project wise dependencies.
5. Make sure you have firefox web browser installed and in your `$PATH`. Else, alias your preferred web browser to `firefox` so that we can open the search results in the browser.

## Usage

Run `python Tokenizer.py` to generate the corpus. Note: Tokenizer is compatible with Python 2 only.

Run `python Search_Query.py` to run the Search GUI. Note: Search_Query is compatible with Python 3 only.

## Features

Following is the list of features we support:

1. Case-insensitive Search Results.
2. Normalisation of query and corpus texts.
3. Ranking of Search Results.
4. Tkinter based UI for Querying.
5. Voice input for search text(experimental).
6. Browsing individual Search Results through clickable links.


# Brown Corpus

We have used Brown Corpus in our project. Here is a brief about it.

> The Brown Corpus of Standard American English was the first of the modern, computer readable, general corpora. It was compiled by W.N. Francis and H. Kucera, Brown University, Providence, RI.

> The corpus consists of one million words of American English texts printed in 1961. The texts for the corpus were sampled from 15 different text categories to make the corpus a good standard reference. Today, this corpus is considered small, and slightly dated. The corpus is, however, still used. Much of its usefulness lies in the fact that the Brown corpus lay-out has been copied by other corpus compilers. The LOB corpus (British English) and the Kolhapur Corpus (Indian English) are two examples of corpora made to match the Brown corpus. The availability of corpora which are so similar in structure is a valuable resourse for researchers interested in comparing different language varieties, for example.

> For a long time, the Brown and LOB corpora were almost the only easily available computer readable corpora. Much research within the field of corpus linguistics has therefore been made using these data. By studying the same data from different angles, in different kinds of studies, researchers can compare their findings without having to take into consideration possible variation caused by the use of different data.

> At the University of Freiburg, Germany, researchers are compiling new versions of the LOB and Brown corpora with texts from 1991. This will undoubtedly be a valuable resource for studies of language change in a near diachronic perspective.

> The Brown corpus consists of 500 texts, each consisting of just over 2,000 words. The texts were sampled from 15 different text categories. The number of texts in each category varies (see below). 

## Tokenizer Code Snippets

The core Tokenizer code that parses and inserts each word in each file into the database. We stem each word using `nltk` before adding to the database. If a word already exists, we increment it's count for that particulat file. For this, we are using a 2d dictionary object to store the data.

```python
 for currentword in content.split():
    ind = currentword.find('/')
    if currentword.find(',')==-1 and currentword.find("'")==-1 and currentword.find('(')==-1:
        currentword = currentword[:ind]
        currentword=currentword.lower()           #Converting each word to small case
        AfterNormalization.add(str(currentword))
        currentword = stemmer.stem(currentword)   #Applying porter stemmer to each word
        BeforeNormalization.add(str(currentword))
        #print currentword
        if dictionary[files].has_key(currentword):
            k=dictionary[files][currentword]
            dictionary[files][currentword]=k+1
        else:
            dictionary[files][currentword]=1
```

Code to construct an inverted index for each word after stemming:

```python
invertedIndex = {}      #to store inverted index for each term

for term in BeforeNormalization:          #Constructing the inverted index
    invertedIndex[term] = []
    for file in fileNames:
        if dictionary[file].has_key(term):
            invertedIndex[term].append(file)
```

Code to calculate TF-IDF for the dataset:

```python
tf_idf = {}

for files in fileNames:
    fileName = 'brown/'+files
    #print files
    tf_idf[str(files)]={}
    for key in dictionary[str(files)]:        #Finding the tf-idf value for each doc
        tf_idf[files][key] = (1 + math.log(dictionary[files][key],10.0) ) * (math.log(n/(1.0 * len(invertedIndex[key]) ), 10.0))
```

The code to dump the generated dataset for use by the querying GUI:

```python
#Dumping all the data structures to be used while querying
pickle.dump( AfterNormalization , open( "AfterNormalization.p", "wb" ) )     
pickle.dump( dictionary , open( "Dictionary.p", "wb" ) )
pickle.dump( tf_idf , open( "Tf_Idf.p", "wb" ) )
pickle.dump( invertedIndex , open( "InvertedIndex.p", "wb" ) )
```

## Querying Code Snippets

We wouldn't go into the glue code for the GUI to work, but would instead focus on the core search code here.

This is the function that calculates the top 10 search results and returns for rendering by the GUI. We first normalize the words and then query from the inverted index for their presence in the text. After that, we calculate the cosine similarity of the query vector with the docs and sort to return the top 10 results.

```python
def Page_Ranking_Algo(query):    #function to implement page ranking
	Query_Dictionary = {}
	Query_List = []

	for word in query.split():  #Representing query as a vector
		word=word.lower()
		word = stemmer.stem(word)
		if word in Query_Dictionary:
			k=Query_Dictionary[word]
			Query_Dictionary[word] = k+1
		else:
			Query_Dictionary[word] = 1

	for key in Query_Dictionary:
		Query_List.append(key)
		print(key)

	score = {}

	# print len(dict)

	for word in Query_List:     #Calculating the cosine similarity of the query vector with the docs
		weight_q = 0
		if word in invertedIndex:
			df = len(invertedIndex[word])
			idf = math.log( N/( df * 1.0 ), 10.0 )
			weight_q = idf * ( 1.0 + math.log( Query_Dictionary[word] , 10.0))

			for doc in invertedIndex[word]:
				if doc in score:
					temp = score[doc]
					weight_d = tf_idf[doc][word]
					score[doc] = temp + weight_q * weight_d
				else:
					weight_d = tf_idf[doc][word]
					score[doc] = weight_q * weight_d

	rank = []

	for key in score:   #Length Normalization of the cosine similarity
		score[key] = score[key]/(1.0 * lengths[key])
		rank.append((key, score[key]))
		#print key, score[key], lengths[key]

	# sorted(ranking,key=itemgetter(1))
	rank = sorted(rank , key=lambda x: x[1], reverse = True)  #sorting all the docs on the basis of their cosine similarity

	print(rank[:10])
	print("*************************************************************************************")
	text = '\n'.join(chunk[0] for chunk in rank[:min(len(rank),10)])  #Returning the top 10 search results
	return text
```
