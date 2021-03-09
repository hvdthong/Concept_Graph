import argparse
from utilities import read_file, filtering_concept
import json
from extraction import extract_text_in_courses
from graph_construct import directed_weighted_graph
from net_graph_construct import net_weight_cover_edges, net_weight_order_edges
import pickle

def read_args():
    parser = argparse.ArgumentParser()
    
    # Construct the cover or order graph    
    parser.add_argument('-title', type=str, help='The dataset contains matching information of course title')    
    parser.add_argument('-section', type=str, help='The dataset contains matching information of course section')
    parser.add_argument('-lecture', type=str, help='The dataset contains matching information of course lecture')
    parser.add_argument('-option', type=str, default='cover', help='Construct the cover or order graph')
    parser.add_argument('-threshold', type=float, default=0.1, help='Construct the cover or order graph')
    return parser

if __name__ == '__main__':
    params = read_args().parse_args()    
    
    if params.option == 'cover':
        if params.title != None and params.section != None:
            edges = directed_weighted_graph(params) 
        else:
            print('If you want to generate the cover graph, please give the matching information of the course title and section')
            exit()
    elif params.option == 'order':
        if params.section != None and params.lecture != None:
            edges = directed_weighted_graph(params) 
        else:
            print('If you want to generate the cover graph, please give the matching information of the course section and lecture')
            exit()
    else:
        print('Please give the correct option of the graph: cover or order')
        exit()
        
    name = params.section.replace('matching_sections_', '').split('/')[-1].split('.')[-2]
    pickle.dump(edges, open(params.option + '_edges_' + name + '.pickle', 'wb'))
    
      
