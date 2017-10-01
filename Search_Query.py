import nltk
import os
import pickle
from nltk.stem.porter import *
import math
import re, collections
import webbrowser
import Tkinter as tk
from Tkinter import *
import Tkinter as tki
from ScrolledText import ScrolledText


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
        if Query_Dictionary.has_key(word):
            k=Query_Dictionary[word]
            Query_Dictionary[word] = k+1
        else:
            Query_Dictionary[word] = 1

    for key in Query_Dictionary:
        Query_List.append(key)
        print key

    score = {}

    # print len(dict)

    for word in Query_List:     #Calculating the cosine similarity of the query vector with the docs
        weight_q = 0
        if invertedIndex.has_key(word):
            df = len(invertedIndex[word])
            idf = math.log( N/( df * 1.0 ), 10.0 )
            weight_q = idf * ( 1.0 + math.log( Query_Dictionary[word] , 10.0))
            
            for doc in invertedIndex[word]:
                if score.has_key(doc):
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

    print rank[:10]
    print "*************************************************************************************"
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
    webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(s)
    

def Show_Results():    #function to show all the relevant documents inside the GUI
    key=entry.get()
    word=key
    text=Page_Ranking_Algo(key)
    print text.split()
    label2 = tk.Label(Text_Area, text=r"*************Results are as follows**************", fg="black", bg="yellow")
    label2.pack()
    label2.bind()
    for words in text.split():
        label1 = tk.Label(Text_Area, text=r"brown/"+words, fg="blue", cursor="hand2")
        label1.pack(fill=X)
        label1.bind("<Button-1>", GotoData)
    label2 = tk.Label(Text_Area, text=r"*************End Of results**************", fg="black", bg="yellow")
    label2.pack()
    label2.bind()
    
Name="Search Engine"

#GUI Window creation

root = Tk()     
root.geometry('500x600')
root.title(Name)

frame1 = Frame(root)
frame1.pack()

entry = completeEntry(frame1)
entry.pack(side=LEFT)
button = Button(frame1, text='Search', width=25, command=Show_Results, bg="#b9eaaf")
button.pack()
entry.focus()

Text_Area = Text(root, wrap='word')
Text_Area.pack(expand='yes', fill='both')
Text_Area['yscrollcommand']=scroll_bar.set
scroll_bar = Scrollbar(Text_Area)
scroll_bar.pack(side=RIGHT, fill=Y)
scroll_bar['command']=Text_Area.yview



root.mainloop()