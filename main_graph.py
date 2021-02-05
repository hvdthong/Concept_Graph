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
    # parser.add_argument('-concept', type=str, help='Directory of the list of concepts')    
    # parser.add_argument('-course', type=str, help='Directory of the list of courses')
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
            matching_title = pickle.load(open(params.title, 'rb'))
            matching_section = pickle.load(open(params.section, 'rb'))
            with open('./data_ver2/dev_web_courses_full.json') as json_file:
                courses = json.load(json_file)
            courses = extract_text_in_courses(courses=courses)
            course_titles = list()
            for c in courses:
                course_titles.append(c['course_id'])
            print(len(set(course_titles)))
            print(len(course_titles))
            # for k in matching_title.keys():
            #     print(len(matching_title[k]))
            # exit()
            print(len(matching_title))
            print(len(matching_section))
            exit()
        else:
            print('Please give the matching information of the course title and section')
            exit()
    elif params.option == 'order':
        pass
    else:
        print('Please give the correct option of the graph: cover or order')
        exit()

    if params.concept != None:
        concepts = read_file(params.concept)        
        concepts = filtering_concept(data=concepts)
    else:
        print('Please give the directory of the list of concepts')
        exit()

    if params.course != None:
        with open(params.course) as json_file:
            courses = json.load(json_file)
        courses = extract_text_in_courses(courses=courses)
    else:
        print('Please give the directory of the list of courses')
        exit()

    if params.option == 'cover' or params.option == 'order':
        edges = directed_weighted_graph(concepts, courses, options=params.option)
        if params.option == 'cover':
            net_edges = net_weight_cover_edges(edges=edges, threshold=params.threshold)
        if params.option == 'order':
            net_edges = net_weight_order_edges(edges=edges, threshold=params.threshold)
    else:
        print('Please give the correct option of the graph: cover or order')
        exit()
    
    pickle.dump(net_edges, open('edges_' + params.course.split('.')[-2].replace('/', ''), 'wb'))
    
      
