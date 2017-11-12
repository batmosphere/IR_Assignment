# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 19:01:49 2017

@author: Tushar Aggarwal
"""

import networkx as nx
import matplotlib.pyplot as plt


file = open('GraphRank.txt')
label = {line[:1]:line[1:].split() for line in file}
print label
file.close()

g = nx.read_edgelist('GraphData.txt',create_using=nx.DiGraph(),nodetype=int)

print nx.info(g)

nx.draw(g,nx.circular_layout(g),with_labels=True, node_color='y',node_size=900,alpha=0.8)

plt.show()

#pos = nx.spring_layout(g)
#nx.draw(g, pos, with_labels=False)
#nx.draw_networkx_labels(g,pos,label)
#nx.draw(g,label, with_labels = True)
#plt.show()