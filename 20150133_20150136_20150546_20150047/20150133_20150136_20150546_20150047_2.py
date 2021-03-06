# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 17:03:02 2017

@author: mukund, tushar
"""






helper.py






from pageRank1 import pageRank
import pandas as pd 
import csv
import operator


links = [[]]

def foo(s):
    try:
        return int(s)
    except ValueError:
        return s
    
file = open("GraphData.txt","w+")

def read_file(filename):
    count=0
    f = open(filename, 'r')
    for line in f:
        (frm, to) =  map(foo, line.split("\t"))
        if(count<=50):
            file.write(`frm`+"\t"+`to`+"\n")
            count+=1
        extend = max(frm - len(links), to - len(links)) + 1
        for i in range(extend):
            links.append([])
        links[frm].append(to)
    f.close()

read_file("web-NotreDame.txt")
#
#pr =  pageRank(links, alpha=0.85, convergence=0.00001, checkSteps=10)
#sum = 0
#f = open("GraphRank.txt","w+")
#for i in range(len(pr)):
#    if(i<50):
#       f.write(`i`+"\t"+`pr[i]`+"\n")
#    print i, "=", pr[i]
#    sum = sum + pr[i]
#print "sum = " + str(sum)
#f.close()


pr =  pageRank(links, alpha=0.85, convergence=0.00001, checkSteps=10)

sum = 0
f = open("GraphRankAll.txt","w+")
for i in range(len(pr)):
   f.write("PageRank of Node" + "\t" +`i` + "\t" + `pr[i]` + "\n")
   print "PageRank of Node", i, "=", pr[i]
   sum = sum + pr[i]
print "sum = " + str(sum)
f.close()

f = open("GraphRank.txt","w+")
for i in range(len(pr)):
    if(i<50):
       f.write("PageRank of Node" + "\t" +`i` + "\t" + `pr[i]` + "\n")
       print "PageRank of Node", i, "=", pr[i]
f.close()

f = open("SortedGraphRank.txt","w+")
sample = open("GraphRankAll.txt")
csv1 = csv.reader(sample,delimiter="\t")
sort = sorted(csv1,key=operator.itemgetter(2))
for i in sort:
    str1 = i[0] + "\t" + i[1] + "\t" + i[2]
    f.write("%s\n" % str1)
f.close()

  









  
pagerank1.py













from numpy import *

def pageRankGenerator( At =[array((),int64)], numLinks=array((),int64), ln=array((),int64),
                            alpha = 0.85, convergence = 0.0001, checkSteps = 10):

    N = len(At)
    M = ln.shape[0]

    iNew = ones((N,), float64) / N
    iOld = ones((N,), float64) / N

    done = False
    while not done:
        iNew /= sum(iNew)

        for step in range(checkSteps):
            iOld, iNew = iNew, iOld
            oneIv = (1 - alpha) * sum(iOld) / N

            oneAv = 0.0
            if M > 0:
                oneAv = alpha * sum(iOld.take(ln, axis = 0)) / N

            ii = 0
            while ii < N:
                page = At[ii]
                h = 0
                if page.shape[0]:
                    h = alpha * dot(
                            iOld.take(page, axis = 0),
                            1. / numLinks.take(page, axis = 0)
                            )
                iNew[ii] = h + oneAv + oneIv
                ii += 1

        diff = sum(abs(iNew - iOld))
        done = (diff < convergence)

        yield iNew


def transposeLinkMatrix(outGoingLinks = [[]]):
    nPages = len(outGoingLinks)
    incomingLinks = [[] for ii in range(nPages)]
    numLinks = zeros(nPages, int64)
    leafNodes = []

    for ii in range(nPages):
        if len(outGoingLinks[ii]) == 0:
            leafNodes.append(ii)
        else:
            numLinks[ii] = len(outGoingLinks[ii])
            for jj in outGoingLinks[ii]:
                incomingLinks[jj].append(ii)

    incomingLinks = [array(ii) for ii in incomingLinks]
    numLinks = array(numLinks)
    leafNodes = array(leafNodes)

    return incomingLinks, numLinks, leafNodes


def pageRank(linkMatrix = [[]],alpha = 0.85,convergence = 0.0001,checkSteps = 10):

    incomingLinks, numLinks, leafNodes = transposeLinkMatrix(linkMatrix)

    for gr in pageRankGenerator(incomingLinks, numLinks, leafNodes,
                                alpha = alpha, convergence = convergence,
                                checkSteps = checkSteps):
        final = gr

    return final












graph.py













import networkx as nx
import matplotlib.pyplot as plt
from random import random

g = nx.read_edgelist('GraphData.txt',create_using=nx.DiGraph(),nodetype=int)

print nx.info(g)

d = nx.degree(g) #for node sizes

colors = [(random(), random(), random()) for _i in range(10)] #for different node colors

nx.draw(g,nx.random_layout(g),with_labels=True,node_size=[v * 300 for v in d.values()], node_color=colors,alpha=0.7)

plt.show()

