import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_edgelist('GraphData.txt',create_using=nx.DiGraph(),nodetype=int)

print nx.info(g)

nx.draw(g,nx.circular_layout(g),with_labels=True, node_color='g',node_size=900,alpha=0.8)

plt.show()
