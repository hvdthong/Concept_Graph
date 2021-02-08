import argparse
from utilities import read_file, filtering_concept
import json
from extraction import extract_text_in_courses
from graph_construct import directed_weighted_graph
from net_graph_construct import net_weight_cover_edges, net_weight_order_edges
import pickle
from graph_construct import concepts_courses_matching_title, concepts_courses_matching_sections, concepts_courses_matching_each_sections

def read_args():
    parser = argparse.ArgumentParser()
    
    # Construct the cover or order graph
    parser.add_argument('-concept', type=str, help='Directory of the list of concepts')    
    parser.add_argument('-course', type=str, help='Directory of the list of courses')    
    return parser

if __name__ == '__main__':
    params = read_args().parse_args()    
    
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
            
    name = params.course.split('/')[-1].split('.')[-2]
    matching_title = concepts_courses_matching_title(concepts, courses)
    pickle.dump(matching_title, open('matching_title_' + name + '.pickle', 'wb'))    
    matching_sections = concepts_courses_matching_sections(concepts, courses)
    pickle.dump(matching_sections, open('matching_sections_' + name + '.pickle', 'wb'))
    matching_each_section = concepts_courses_matching_each_sections(concepts, courses)
    pickle.dump(matching_each_section, open('matching_each_section_' + name + '.pickle', 'wb'))
    
    
      
