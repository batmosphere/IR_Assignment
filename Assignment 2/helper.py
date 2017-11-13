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
        if(count<50):
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


    
