import argparse
import pickle
from tree_graph import extract_nodes, checking_concept, tree_concept

def read_args():
    parser = argparse.ArgumentParser()
    
    # Construct the cover or order graph
    parser.add_argument('-concept', type=str, help='Name of the concept')    
    parser.add_argument('-graph_edge', type=str, help='Directory of the list of edges in the graph')
    return parser

if __name__ == '__main__':
    params = read_args().parse_args()

    if params.edge != None:        
        edges = pickle.load(open(params.edge, 'rb'))
    else:
        print('Please give the directory of the list of edges')
        exit()

    if params.concept != None:
        pass
    else:
        print('Please give the concept name')
        exit()

    nodes = extract_nodes(edges)
    flag, concept = checking_concept(params.concept, nodes)
    if flag:
        pass
    else:
        print('Please give the correct concept name')
        exit()

    root_edges = tree_concept(concept=concept, edges=edges)    
    pickle.dump(root_edges, open(concept.split(',')[0] + '_' + params.edge.split('.')[-2].replace('/', '') + '.pickle', 'wb'))
