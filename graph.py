#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
import pickle

edges = pickle.load(open('edges.pickle', 'rb'))

G = nx.Graph()
G.add_edges_from(edges)

pos = nx.layout.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=1)
nx.draw_networkx_edges(G, pos, width=1)
#nx.draw_networkx_labels(G, pos, font_size=1, font_family='sans-serif')

plt.axis('off')
plt.show()
