import networkx as nx
import matplotlib.pyplot as plt
from random import random

g = nx.read_edgelist('GraphData.txt',create_using=nx.DiGraph(),nodetype=int)

print nx.info(g)

d = nx.degree(g) #for node sizes

colors = [(random(), random(), random()) for _i in range(10)] #for different node colors

nx.draw(g,nx.random_layout(g),with_labels=True,node_size=[v * 300 for v in d.values()], node_color=colors,alpha=0.7)

plt.show()
