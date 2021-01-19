import re 
from tqdm import tqdm

def regular_expression_for_concept(concept, text):
    reg = r'\b' + re.escape(concept) + r's*' + r'\b'
    matched = re.findall(reg, text, re.IGNORECASE)
    matched_count = len(matched)
    return matched, matched_count

def match_each_concept_with_each_course_title(concept, title):
    concept = [con.strip() for con in concept.split(',')]
    flag = False
    for con in concept:
        match_freq = regular_expression_for_concept(concept=con, text=title)[1]
        if match_freq > 0:
            flag = True
            title = title.replace(con, '').strip()
    if flag:
        return True, title
    return False, title

def concepts_courses_matching_title(concepts, courses):
    matching_course = dict()
    print('Matching concepts with the course title')
    for course in tqdm(courses):
        matching_course[course['course_title']] = {}
        title = course['course_title'].lower()
        for concept in concepts:
            matching, update_title = match_each_concept_with_each_course_title(concept, title)            
            title = update_title
            if matching:                
                matching_course[course['course_title']][concept] = True
            else:
                matching_course[course['course_title']][concept] = False    
    return matching_course

def extract_concept_in_section_heading(concept, sections):
    # Section heading = Section title 
    freq = 0
    update_sections = list()
    for sec in sections:
        if regular_expression_for_concept(concept=concept, text=sec)[1] > 0:            
            freq += regular_expression_for_concept(concept=concept, text=sec)[1]
            update_sections.append(sec.lower().replace(concept, '').strip())
        else:
            update_sections.append(sec)
    return freq, update_sections

def extract_concept_in_section_description(concept, sections_desc):
    freq = 0
    update_secs_desc = list()
    for sec in sections_desc:
        lecs_title = sec['title']
        lecs_description = sec['description']

        freq_title, update_lecs_title = extract_concept_in_section_heading(concept=concept, sections=lecs_title)
        freq_desc, update_lecs_desc = extract_concept_in_section_heading(concept=concept, sections=lecs_description)

        update_sec = dict()
        update_sec['title'] = update_lecs_title
        update_sec['description'] = update_lecs_desc
        update_secs_desc.append(update_sec)

        freq += freq_title
        freq += freq_desc
    return freq, update_secs_desc

def match_each_concept_with_course_sections(concept, sections_headline, sections_desc):
    # Note that one course may have multiple sections
    concept = [con.strip() for con in concept.split(',')]
    flag = False
    for con in concept:
        freq_sec_heading, update_secs_headline = extract_concept_in_section_heading(concept=con, sections=sections_headline)
        freq_sec_desc, update_secs_desc = extract_concept_in_section_description(concept=con, sections_desc=sections_desc)
        if freq_sec_heading > 0:
            flag = True
            sections_headline = update_secs_headline
        if freq_sec_desc > 0:
            flag = True
            sections_desc = update_secs_desc
    if flag == True:
        return True, sections_headline, sections_desc
    return False, sections_headline, sections_desc    

def concepts_courses_matching_sections(concepts, courses):
    matching_course = dict()
    print('Matching concepts with the multiple sections of the course')
    for course in tqdm(courses):
        matching_course[course['course_title']] = {}
        sections_headline, sections_desc = course['sections'], course['sections_desc']
        for concept in concepts:
            matching, update_secs_headline, update_secs_desc = match_each_concept_with_course_sections(concept, sections_headline, sections_desc)
            if matching:                
                matching_course[course['course_title']][concept] = True
                sections_headline = update_secs_headline
                sections_desc = update_secs_desc
            else:
                matching_course[course['course_title']][concept] = False
    return matching_course

def edge_cover(root_node, dest_node, courses, N_sup, concepts, matching_title, matching_sections):
    titles = [c['course_title'] for c in courses]
    root_node_course_title, numerator = 0, 0

    for key in titles:
        if matching_title[key][root_node] == True:
            root_node_course_title += 1

    for key in titles:
        if matching_title[key][root_node] == True and matching_sections[key][dest_node] == True:
            numerator += 1

    if root_node_course_title != 0:
        denominator = max(N_sup, root_node_course_title) + 1
        return (numerator + (1 / len(concepts))) / denominator
    else:
        return 0

def match_concept_with_course_each_section(concept, section_headline, section_desc):
    concept = [con.strip() for con in concept.split(',')]
    flag = False
    lecs_title, lecs_desc = section_desc['title'], section_desc['description']
    for con in concept:        
        freq_title = regular_expression_for_concept(con, section_headline)[1]
        freq_lecs_title, update_lecs_title = extract_concept_in_section_heading(con, lecs_title)
        freq_lecs_desc, update_lecs_desc = extract_concept_in_section_heading(con, lecs_desc)
        if freq_title > 0:
            flag = True
            section_headline = section_headline.lower().replace(con, '').strip()
        if freq_lecs_title > 0:
            flag = True
            lecs_title = update_lecs_title
        if freq_lecs_desc > 0:
            flag = True
            lecs_desc = update_lecs_desc

    if flag:
        new_section_desc = dict()
        new_section_desc['title'], new_section_desc['description'] = lecs_title, lecs_desc
        return True, section_headline, new_section_desc
    return False, section_headline, section_desc

def concepts_courses_matching_each_sections(concepts, courses):
    matching_course = dict()
    print('Matching concepts with the description in the section')
    for course in tqdm(courses):
        matching_course[course['course_title']] = {}
        # for concept in concepts:
        #     match_sections = list()
        #     for i in range(len(course['sections'])):
        #         if match_concept_with_course_each_section(concept, course['sections'][i], course['sections_desc'][i]):
        #             match_sections.append(i)
        #     matching_course[course['course_title']][concept] = match_sections
        
        for i in range(len(course['sections'])):
            sec_headline = course['sections'][i]
            sec_desc = course['sections_desc'][i]
            for concept in concepts:
                matching, update_sec_headline, update_sec_desc = match_concept_with_course_each_section(concept, sec_headline, sec_desc)
                if matching: 
                    if concept not in matching_course[course['course_title']].keys():
                        matching_course[course['course_title']][concept] = [i]
                    else:
                        matching_course[course['course_title']][concept].append(i)

                    sec_headline = update_sec_headline
                    sec_desc = update_sec_desc
                else:
                    matching_course[course['course_title']][concept] = []
    return matching_course

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

def directed_weighted_graph(concepts, courses, options):    
    if options == 'cover':
        matching_title = concepts_courses_matching_title(concepts, courses)
        matching_sections = concepts_courses_matching_sections(concepts, courses)
        N_sup = len([c['course_title'] for c in courses]) / 20

        edges = list()
        for i in range(len(concepts)):
            root_node = concepts[i]
            for j in range(len(concepts)):
                edge = list()
                dest_node = concepts[j]
                if root_node != dest_node:
                    weight = edge_cover(root_node, dest_node, courses, N_sup, concepts, matching_title, matching_sections)
                    if weight > 0:
                        edge.append(root_node)
                        edge.append(dest_node)
                        edge.append(weight)
                        edges.append(edge)    
    if options == 'order':
        matching_sections = concepts_courses_matching_sections(concepts, courses)
        matching_each_section = concepts_courses_matching_each_sections(concepts, courses)
        N_sup = len([c['course_title'] for c in courses]) / 20

        edges = list()
        for i in range(len(concepts)):
            root_node = concepts[i]
            for j in range(len(concepts)):
                edge = list()
                dest_node = concepts[j]
                if root_node != dest_node:
                    weight = edge_order(root_node, dest_node, courses, N_sup, concepts, matching_sections, matching_each_section)
                    if weight > 0:
                        edge.append(root_node)
                        edge.append(dest_node)
                        edge.append(weight)
                        edges.append(edge)
    return edges