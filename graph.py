#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
import pickle

def main():
    connections = pickle.load(open('connections.pickle', 'rb'))

    edges = []
    for connection in connections:
        edge = (connection['local_addr'], connection['peer_addr'], connection)
        edge[2]['weight'] = connection['rtt_avg']
        edges.append(edge)

    G = nx.Graph()
    G.add_edges_from(edges)

    pos = nx.layout.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=1)
    nx.draw_networkx_edges(G, pos, width=1)
    #nx.draw_networkx_labels(G, pos, font_size=1, font_family='sans-serif')

    plt.axis('off')
    plt.gcf().set_size_inches(32, 24)
    plt.savefig('graph.png', dpi=96)
    plt.show()

if __name__ == '__main__':
    main()
