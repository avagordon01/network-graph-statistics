#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
import pickle

def main():
    connections = pickle.load(open('connections.pickle', 'rb'))

    address_pid_map = {}
    for connection in connections:
        address_pid_map[connection['local_addr']] = connection['local_pid']

    edges = []
    for connection in connections:
        interested = False
        for user in connection['users']:
            interested = user['name'] in ['1', '2', '3', '4', '5', '6']
            if interested:
                break
        if not interested:
            continue
        edge = (connection['local_addr'], connection['peer_addr'], connection)
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
