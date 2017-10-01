import nltk
import os
import pickle
from nltk.stem.porter import *
import math
fileNames = os.listdir('brown')  #to list the name of all the docs inside the brown corpus

stemmer = PorterStemmer()   #object for porter stemmer

dictionary = {}       #to store term frequency of each file
BeforeNormalization = set()       #to store all the distinct word before normalization
AfterNormalization = set()      #to store all the distinct word after normalization


for files in fileNames:
    fileName = 'brown/'+files
    #print files
    dictionary[str(files)]={}
    with open(fileName) as f:       #Reading all the files word by word
        content = f.read()
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

print "Number of words after Normalization and Stemming : " + str(len(AfterNormalization))

invertedIndex = {}      #to store inverted index for each term

for term in BeforeNormalization:          #Constructing the inverted index
    invertedIndex[term] = []
    for file in fileNames:
        if dictionary[file].has_key(term):
            invertedIndex[term].append(file)
           

n = len(fileNames)

tf_idf = {}

for files in fileNames:
    fileName = 'brown/'+files
    #print files
    tf_idf[str(files)]={}
    for key in dictionary[str(files)]:        #Finding the tf-idf value for each doc
        tf_idf[files][key] = (1 + math.log(dictionary[files][key],10.0) ) * (math.log(n/(1.0 * len(invertedIndex[key]) ), 10.0))

#Dumping all the data structures to be used while querying
pickle.dump( AfterNormalization , open( "AfterNormalization.p", "wb" ) )     
pickle.dump( dictionary , open( "Dictionary.p", "wb" ) )
pickle.dump( tf_idf , open( "Tf_Idf.p", "wb" ) )
pickle.dump( invertedIndex , open( "InvertedIndex.p", "wb" ) )
