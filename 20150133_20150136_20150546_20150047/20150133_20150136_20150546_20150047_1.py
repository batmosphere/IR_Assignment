# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:04:14 2017

@author: mukund
"""







Search_Query.py







import nltk
import os
import pickle
from nltk.stem.porter import *
import math
import re, collections
import webbrowser
import tkinter as tk
from tkinter import *
import speech_recognition as sr
import pyttsx3 as pyttsx


lengths = {}

stemmer = PorterStemmer()

#Loading all the data structures created before
dict = pickle.load(open("Dictionary.p","rb"))
invertedIndex = pickle.load(open("InvertedIndex.p","rb"))
tf_idf = pickle.load(open("Tf_Idf.p","rb"))


N = len(dict)

for key in tf_idf:  #Finding the length of each vector(doc represented as a vector)
	temp = 0.0
	for word in tf_idf[key]:
		temp = temp + tf_idf[key][word] * tf_idf[key][word]
	lengths[key] = math.sqrt(temp)


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


class completeEntry(Entry):
	def __init__(self,*args, **args2):
		Entry.__init__(self, *args, **args2)
		self.var = self["textvariable"]
		if self.var == '':
			self.var = self["textvariable"] = StringVar()

def GotoData(event):    #function which gets called when a doc link is clicked
	s = event.widget.cget("text")
	webbrowser.get("firefox").open(s)


def Show_Results():    #function to show all the relevant documents inside the GUI
	key=entry.get()
	word=key
	text=Page_Ranking_Algo(key)
	print(text.split())

	engine = pyttsx.init()		#Text to Speech Engine using pyttsx library
	rate = engine.getProperty('rate')
	engine.setProperty('rate', rate-40)
	engine.setProperty('voice', 'english+f3')
	engine.say('The Top 10 results are as follows')
	engine.runAndWait()

	for words in text.split():
		label1 = tk.Label(Text_Area, text=r"brown/"+words, fg="blue", cursor="hand2")
		label1.pack(fill=X)
		label1.bind("<Button-1>", GotoData)
	label2 = tk.Label(Text_Area, text=r"***************************", fg="black", bg="yellow")
	label2.pack()
	label2.bind()


def SpeechToText():     #function to implement speach to text conversion
												 # obtain audio from the microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)

	# recognize speech using Sphinx
	try:
		print("Sphinx thinks you said " + r.recognize_sphinx(audio))
		key = r.recognize_sphinx(audio)		#pyaudio library required
		#entry = StringVar()
		#entry.set(str1)
		#showSearchResults()
		entry.delete(0, END)
		entry.insert(0,key)
		word=key
		text=pageRank(key)
		content_text.delete('1.0', END)
		content_text.insert('0.0',text)
	except sr.UnknownValueError:
			print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))


Name="Search Engine IR Assignment 1"

#GUI Window creation

root = Tk()
root.geometry('500x600')
root.title(Name)

frame1 = Frame(root)
frame1.pack()

entry = completeEntry(frame1)
entry.pack(side=LEFT)
button = Button(frame1, text='Search', width=25, command=Show_Results, bg="#b9eaaf")
button.pack(side=LEFT)
button = Button(frame1, text='Speak Now', width=10, command=SpeechToText)
button.pack(side=LEFT)
entry.focus()

Text_Area = Text(root, wrap='word')
Text_Area.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(Text_Area)
Text_Area['yscrollcommand']=scroll_bar.set
scroll_bar.pack(side=RIGHT, fill=Y)
scroll_bar['command']=Text_Area.yview



root.mainloop()













Tokenizer.py














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
















Alternative IR assignment 1











search.js










'use strict';

const fs = require('fs-extra');
const path = require('path');
let glob = require('glob'); // use let so that it can be updated by promisify();
const natural = require('natural');

const config = require('./config');

const CACHE_FOLDER = path.join(config.get().cache, 'cache');

const filepath = CACHE_FOLDER + '/search-corpus.json';

let corpus = {};

corpus.fileWords = {};
corpus.fileLengths = {};
corpus.invertedIndex = {};
corpus.allTokens = new Set(); // eslint-disable-line
corpus.tfidf = {};

let query = {};

query.raw = null;
query.tokens = null;
query.frequency = {};
query.score = {};
query.ranks = [];

let promisify = () => {
  fs.readFileAsync = (filename, encoding) => {
    return new Promise((resolve, reject) => {
      fs.readFile(filename, encoding, (err, data) => {
        if (err)
        {reject(err);}
        else
        {resolve(data);}
      });
    });
  };
  fs.writeFileAsync = (filename, data, encoding) => {
    return new Promise((resolve, reject) => {
      fs.writeFile(filename, data, encoding, (err, data) => {
        if (err)
        {reject(err);}
        else
        {resolve(data);}
      });
    });
  };
  let globSync = glob;
  glob = (string, options) => {
    return new Promise((resolve, reject) => {
      globSync(string, options, (err, data) => {
        if (err)
        {reject(err);}
        else
        {resolve(data);}
      });
    });
  };
};
promisify();

let getTokens = (data) => {
  let tokenizer = new natural.WordTokenizer();
  let tokens = tokenizer.tokenize(data);
  tokens.forEach((word, index) => {
    word = word.toLowerCase();
    word = natural.PorterStemmer.stem(word);
    tokens[index] = word;
  });

  return tokens;
};

let createFileIndex = (tokens, name) => {
  corpus.fileWords[name] = {};
  tokens.forEach(word => {
    corpus.allTokens.add(word);
    if (corpus.fileWords[name][word]) { // Word already exists. Increment count.
      corpus.fileWords[name][word]++;
    } else {
      corpus.fileWords[name][word] = 1;
    }
  });
};

let createInvertedIndex = (tokens) => {
  tokens.forEach(word => {
    Object.keys(corpus.fileWords).forEach(name => {
      if (corpus.fileWords[name][word]) {
        if (corpus.invertedIndex[word]) {
          corpus.invertedIndex[word].push(name);
        } else {
          corpus.invertedIndex[word] = [name];
        }
      }
    });
  });
};

let getTf = (word, filename) => {
  let worddata = corpus.fileWords[filename];
  let frequency = worddata[word] || 0;
  let length = 0;
  Object.keys(worddata).forEach(key => {
    length += worddata[key];
  });
  let tf = frequency / length;
  return tf;
};

let getIdf = (word) => {
  let allFiles = Object.keys(corpus.fileWords).length;
  let wordFiles = corpus.invertedIndex[word].length;
  let idf = Math.log(allFiles / wordFiles);
  return idf;
};

let createTfIdf = () => {
  corpus.tfidf = {};
  Object.keys(corpus.fileWords).forEach(file => {
    corpus.tfidf[file] = {};
    Object.keys(corpus.fileWords[file]).forEach(word => {
      let tfidf = getTf(word, file) * getIdf(word);
      corpus.tfidf[file][word] = tfidf;
    });
  });
};

let processRawDocument = (data, name) => {
  let tokens = getTokens(data);
  createFileIndex(tokens, name);    //creates word frequency data
};

let createFileLengths = () => {
  Object.keys(corpus.tfidf).forEach(name => {
    let len = 0;
    Object.keys(corpus.tfidf[name]).forEach(word => {
      len += corpus.tfidf[name][word] * corpus.tfidf[name][word];
    });
    corpus.fileLengths[name] = Math.sqrt(len);
  });
};

let writeCorpus = () => {
  corpus.allTokens = Array.from(corpus.allTokens);
  let json = JSON.stringify(corpus);
  return fs.writeFileAsync(filepath, json, 'utf8').then(() => {
    return Promise.resolve('JSON written to disk at: ' + filepath);
  });
};

let readCorpus = () => {
  return fs.readFileAsync(filepath, 'utf8').then(data => {
    corpus = JSON.parse(data.toString());
    return Promise.resolve();
  });
};

let processQuery = (rawquery) => {
  query.raw = rawquery;
  query.tokens = getTokens(rawquery);
  query.frequency = {};
  query.tokens.forEach(word => {
    if (query.frequency[word]) { // Word already exists. Increment count.
      query.frequency[word]++;
    } else {
      query.frequency[word] = 1;
    }
  });
  let numberOfFiles = Object.keys(corpus.fileWords).length;
  query.score = {};
  query.tokens.forEach(word => {
    if (corpus.invertedIndex[word]) {
      let df = corpus.invertedIndex[word].length;
            let idf = Math.log(numberOfFiles / df, 10); // eslint-disable-line
            let wordWeight = idf * (1 + Math.log(query.frequency[word], 10)); // eslint-disable-line
      corpus.invertedIndex[word].forEach(file => {
        let fileWeight = corpus.tfidf[file][word];
        if (query.score[file]) {
          query.score[file] += fileWeight * wordWeight;
        } else {
          query.score[file] = fileWeight * wordWeight;
        }
      });
    }
  });
  Object.keys(query.score).forEach(file => {
    query.score[file] = query.score[file] / corpus.fileLengths[file];
    let rankobj = {};
    rankobj.file = file;
    rankobj.score = query.score[file];
    query.ranks.push(rankobj);
  });
  query.ranks.sort((a, b) => {
    if (a.score > b.score) {
      return -1; // eslint-disable-line
    } 
    if (a.score < b.score) {
      return 1;
    }
    return 0;
  });
};


// This function creates an index from the corpus

exports.createIndex = () => {
  glob(CACHE_FOLDER + '/pages/**/*.md', {}).then(files => {
//        let testfiles = files.slice(100, 102); // eslint-disable-line
    let promises = [];
    files.forEach(file => {
      let promise = fs.readFileAsync(file).then((data) => {

        // processRawDocument finds the frequency of each file using tokenization and stemming
        
        processRawDocument(data.toString(), file); 
      });
      promises.push(promise);
    });
    
    //the following code executes after all files are loaded

    Promise.all(promises).then(() => {
      createInvertedIndex(corpus.allTokens);
      createTfIdf();
      createFileLengths();
      return writeCorpus();
    //index generation completed, program exits
    }).then(() => {
      console.log('Done');
    }).catch(error => {
      console.error('Error in creating corpus. Exiting.');
      console.error(error.message);
      console.error(error.stack);
    });
  });
};

exports.getResults = (rawquery) => {
  readCorpus().then(() => {
    // all the handling of results is done in this function
    processQuery(rawquery);
    //display top 10 results only
    let results = query.ranks.slice(0, 10); // eslint-disable-line
    console.log(results);
  });
};