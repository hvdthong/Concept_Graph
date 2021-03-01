import re 
from tqdm import tqdm
import pickle
from functools import partial
from functools import partial
from multiprocessing import Pool

def regular_expression_for_concept(concept, text):
    concept = '|'.join(concept).strip()
    reg = r'\b' + re.escape(concept) + r's*' + r'\b'    
    matched = bool(re.search(reg, text, re.IGNORECASE))    
    return matched

def filtering_concept(concept):
    concept = concept.split(',')
    new_concept = list()
    for con in concept:
        if len(con.strip()) > 0:
            new_concept.append(con.strip())
    return new_concept

def match_each_concept_with_each_course_title(concept, title):
    concept = filtering_concept(concept)
        
    if regular_expression_for_concept(concept=concept, text=title) == True:        
        title = re.sub(r'|'.join(map(re.escape, concept)), '', title).strip()
        return True, title
    else:
        return False, title

def multiprocessing_title(course, concepts):
    matching_course = dict()
    matching_course[course['course_id']] = {}
    title = course['course_title'].lower()
    title = course['course_title'].lower()

    for concept in concepts:
        matching, update_title = match_each_concept_with_each_course_title(concept, title)            
        title = update_title
        if matching:                
            matching_course[course['course_id']][concept] = True
        else:
            matching_course[course['course_id']][concept] = False           
    return matching_course

def concepts_courses_matching_title(concepts, courses, params):
    print('Matching concepts with the course title')
    pool = Pool(processes=params.p)
    results = pool.map(partial(multiprocessing_title, concepts=concepts), tqdm(courses))
    pool.close()
    new_results = {}
    for r in results:
        new_results.update(r)
    return new_results

def extract_text_sections_headline(sections):
    text = ' '.join(sections).strip()
    return text.lower()

def extract_text_sections_desc(sections_desc):
    title_text, desc_text = '', ''

    for sec in sections_desc:        
        title_text += ' ' + ' '.join(sec['title'])
        desc_text += ' ' + ' '.join(sec['description'])
        title_text = title_text.strip()
        desc_text = desc_text.strip()
    return (title_text + ' ' + desc_text).lower()

def multiprocessing_section(course, concepts):
    matching_course = dict()
    matching_course[course['course_id']] = {}
    sections_headline, sections_desc = course['sections'], course['sections_desc']
    sections_headline = extract_text_sections_headline(sections_headline)
    sections_desc = extract_text_sections_desc(sections_desc)
    sections_text = sections_headline + sections_desc

    for concept in concepts:
        matching, update_sections = match_each_concept_with_each_course_title(concept, sections_text)            
        sections_text = update_sections
        if matching:                
            matching_course[course['course_id']][concept] = True
        else:
            matching_course[course['course_id']][concept] = False   
    return matching_course


def concepts_courses_matching_sections(concepts, courses, params):
    print('Matching concepts with the multiple sections of the course')
    pool = Pool(processes=params.p)
    results = pool.map(partial(multiprocessing_section, concepts=concepts), tqdm(courses))
    pool.close()
    new_results = {}
    for r in results:
        new_results.update(r)
    return new_results


def extract_text_each_sections_decs(section_desc):    
    title_text = ' '.join(section_desc['title'])
    desc_text = ' '.join(section_desc['description'])
    return (title_text + ' ' + desc_text).strip()


def multiprocessing_each_section(course, concepts):
    matching_course = dict()
    matching_course[course['course_id']] = {}
    
    for i in range(len(course['sections'])):        
        sec_headline = course['sections'][i]
        sec_desc = course['sections_desc'][i]
        sec_text = (sec_headline + ' ' + extract_text_each_sections_decs(sec_desc)).lower()

        for concept in concepts:
            matching, update_sec_text = match_each_concept_with_each_course_title(concept, sec_text)            
            sec_text = update_sec_text
            if matching:                
                if concept not in matching_course[course['course_id']].keys():
                    matching_course[course['course_id']][concept] = [i]
                else:
                    matching_course[course['course_id']][concept].append(i)
            else:
                matching_course[course['course_id']][concept] = []
    return matching_course

def concepts_courses_matching_each_sections(concepts, courses, params):
    print('Matching concepts with the description in the section')
    pool = Pool(processes=params.p)
    results = pool.map(partial(multiprocessing_each_section, concepts=concepts), tqdm(courses))
    pool.close()
    new_results = {}
    for r in results:
        new_results.update(r)
    return new_results

def edge_cover(root_node, dest_node, courses, N_sup, concepts, matching_title, matching_sections):    
    root_node_course_title, numerator = 0, 0

    # for key in titles:
    for key in matching_title.keys():
        if matching_title[key][root_node] == True:
            root_node_course_title += 1
            if matching_sections[key][dest_node] == True:
                numerator += 1

    if root_node_course_title != 0:
        denominator = max(N_sup, root_node_course_title) + 1
        return (numerator + (1 / len(concepts))) / denominator
    else:
        return 0

def edge_order(root_node, dest_node, courses, N_sup, concepts, matching_sections, matching_each_section):
    titles = [c['course_title'] for c in courses]
    denominator, numerator = 0, 0

    for key in titles:
        if matching_sections[key][root_node] == True:
            denominator += 1
    
    for key in titles:
        root_node_each_section = matching_each_section[key][root_node]
        dest_node_each_section = matching_each_section[key][dest_node]

        if (len(root_node_each_section) > 0) and (len(dest_node_each_section) > 0):
            if min(root_node_each_section) < max(dest_node_each_section):
                numerator += 1

    denominator = max(N_sup, denominator) + 1
    return (numerator + (1 / len(concepts))) / denominator

def converting_structured_for_title_section(data):
    courses = data.keys()
    concepts = list()
    for k in data.keys():
        concepts = data[k]
        break

    new_dict = dict()
    for concept in concepts:        
        new_course = list()
        for course in courses:
            if data[course][concept] == True:
                new_course.append(course)
        new_dict[concept] = new_course
    return new_dict

def converting_structured_for_each_section(data):
    filter_data = dict()
    for k in data.keys():        
        if len(data[k].keys()) > 0:
            filter_data[k] = data[k]   

    courses = filter_data.keys()
    concepts = list()
    for k in courses:
        concepts = filter_data[k]
        break    
    
    new_dict = dict()
    for concept in concepts:        
        new_course = dict()
        for course in courses:
            if len(filter_data[course][concept]) > 0:
                new_course[course] = filter_data[course][concept]
        if len(new_course) > 0:
            new_dict[concept] = new_course
    return new_dict

def directed_weighted_graph(params):
    edges = list()
    if params.option == 'cover':
        matching_title = pickle.load(open(params.title, 'rb'))
        matching_section = pickle.load(open(params.section, 'rb'))

        
        N_sup = len(matching_title.keys()) / 20
        matching_title = converting_structured_for_title_section(data=matching_title)
        matching_section = converting_structured_for_title_section(data=matching_section)
        num_concepts = len(matching_title.keys())

        for root_node in matching_title.keys():
            for dest_node in matching_title.keys():
                edge = list()
                if root_node != dest_node:

                    if len(matching_title[root_node]) > 0 and len(matching_section[dest_node]) > 0:
                        root_node_course_title = len(matching_title[root_node])                        
                        numerator = len(list(set(matching_title[root_node]) & set(matching_section[dest_node])))
                        denominator = max(N_sup, root_node_course_title) + 1
                        weight = (numerator + (1 / num_concepts)) / denominator
                        if weight > params.threshold:
                            edge.append(root_node)
                            edge.append(dest_node)
                            edge.append(weight)
                            edges.append(edge)
    
    if params.option == 'order':
        matching_section = pickle.load(open(params.section, 'rb'))
        matching_each_section = pickle.load(open(params.lecture, 'rb'))        

        N_sup = len(matching_section.keys()) / 20
        matching_section = converting_structured_for_title_section(data=matching_section)
        matching_each_section = converting_structured_for_each_section(data=matching_each_section)
        num_concepts = len(matching_section.keys())
        
        for root_node in matching_each_section.keys():
            for dest_node in matching_each_section.keys():
                edge = list()
                if root_node != dest_node: 
                    if len(matching_section[root_node]) > 0:
                        denominator = len(matching_section[root_node]) 
                        numerator = 0
                        root_node_course = matching_each_section[root_node].keys()
                        dest_node_course = matching_each_section[dest_node].keys()

                        intersect_course = list(set(root_node_course) & set(dest_node_course))
                        if len(intersect_course) > 0:
                            for course in intersect_course:
                                if min(matching_each_section[root_node][course]) < max(matching_each_section[dest_node][course]):                                    
                                    numerator += 1
                        
                            denominator = max(N_sup, denominator) + 1
                            weight = (numerator + (1 / num_concepts)) / denominator
                            if weight > params.threshold:
                                edge.append(root_node)
                                edge.append(dest_node)
                                edge.append(weight)
                                edges.append(edge)           
    return edges                       