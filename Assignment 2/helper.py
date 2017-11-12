import sys
from pageRank1 import pageRank

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

pr =  pageRank(links, alpha=0.85, convergence=0.00001, checkSteps=10)
sum = 0
f = open("GraphRank.txt","w+")
for i in range(len(pr)):
    if(i<50):
       f.write(`i`+"\t"+`pr[i]`+"\n")
    print i, "=", pr[i]
    sum = sum + pr[i]
print "sum = " + str(sum)
f.close()

