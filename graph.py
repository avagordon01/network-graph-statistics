#!/usr/bin/env python3

import pickle
import json

def main():
    connections = pickle.load(open('connections.pickle', 'rb'))

    address_pid_map = {}
    for connection in connections:
        address_pid_map[connection['local_addr']] = connection['local_pid']
        if connection['peer_addr'] and connection['peer_pid']:
            address_pid_map[connection['peer_addr']] = connection['peer_pid']

    print(address_pid_map)
    nodes = []
    edges = []
    for connection in connections:
        #smaller weight = further apart
        connection['weight'] = 1 / connection['rtt_avg']
        if not connection['users']:
            continue
        local_pid = address_pid_map[connection['local_addr']]
        if connection['peer_addr'] in address_pid_map:
            peer_pid = address_pid_map[connection['peer_addr']]
            edges.append({'source': str(local_pid), 'target': str(peer_pid), **connection})
            nodes.append({'id': str(peer_pid)})
        else:
            edges.append({'source': str(local_pid), 'target': connection['peer_addr'], **connection})
            nodes.append({'id': str(connection['peer_addr'])})
        nodes.append({'id': str(local_pid), **connection['users'][0]})

    json_graph = {'nodes': nodes, 'links': edges}
    with open('data.json', 'w') as outfile:
        json.dump(json_graph, outfile)

if __name__ == '__main__':
    main()
