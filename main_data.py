import argparse
import pickle
from graph_data import json_node, json_links 
import json

def read_args():
    parser = argparse.ArgumentParser()
    
    # Construct the json data for the edges 
    parser.add_argument('-edge', type=str, help='Directory of the list of edges')        
    return parser

if __name__ == '__main__':
    params = read_args().parse_args()

    if params.edge != None:        
        edges = pickle.load(open(params.edge, 'rb'))
    else:
        print('Please give the directory of the list of edges')
        exit()

    data = {'nodes': json_node(edges=edges), 'links': json_links(edges=edges)}
    name = params.edge.split('.')[-2].replace('/', '')
    json.dump(data, open(name + '.json', "w"))