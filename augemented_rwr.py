import numpy as np 
from tree_graph import extract_nodes
from rwr.RWR import RWR

def convert_edges_to_numpy(edges):
    nodes = extract_nodes(edges)

    new_edges = list()
    for edge in edges:
        new_edges.append(np.array([nodes.index(edge[0]), nodes.index(edge[1]), edge[2]]))
    return np.array(new_edges)

def run_rwr(edges, params):
    nodes = extract_nodes(edges)
    edges = convert_edges_to_numpy(edges)

    rwr_edges = list()
    rwr = RWR()
    rwr.read_graph(edges, 'directed')
    for i in range(0, len(nodes)):
        seed = i
        r = list(rwr.compute(seed, params.c, params.epsilon, params.max_iters))
        for j in range(len(r)):
            edge = list()
            w = r[j]
            if j != i and w > 0:
                edge.append(nodes[i])
                edge.append(nodes[j])
                edge.append(w)
                rwr_edges.append(edge)
    return rwr_edges