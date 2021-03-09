import argparse
from augemented_rwr import run_rwr
import pickle

def read_args():
    parser = argparse.ArgumentParser()
        
    parser.add_argument('-graph_edge', type=str, help='Directory of the list of edges in the graph')
    parser.add_argument('-c', type=float, default=0.15, help='Restart probablity (rwr) or jumping probability (otherwise)')
    parser.add_argument('-epsilon', type=float, default=1e-9, help='Error tolerance for power iteration')
    parser.add_argument('-max_iters', type=int, default=100, help='Maximum number of iterations for power iteration')    
    return parser

if __name__ == '__main__':
    params = read_args().parse_args()

    if params.edge != None:        
        edges = pickle.load(open(params.edge, 'rb'))
    else:
        print('Please give the directory of the list of edges in the graph')
        exit()
    
    rwr_edges = run_rwr(edges, params)
    pickle.dump(rwr_edges, open('rwr_' + params.edge.split('.')[-2].replace('/', '') + '.pickle', 'wb'))