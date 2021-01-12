import re 

def remove_html_tags(text):
    # """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract_title_in_course(course):
    return course['course_title'].lower()    

def extract_section_in_course(course, option):
    if option == 'section':
        sections = list()
        for sec in course['course_content']['section']:
            sections.append(sec['title'].lower())
        return sections
    elif option == 'section_desc':
        sections_desc = list()
        for sec in course['course_content']['section']:
            items = sec['items']
            lecture = dict()
            lec_title, lec_desc = list(), list()
            for item in items:
                lec_title.append(item['title'])
                if item['description'] != None:
                    lec_desc.append(remove_html_tags(item['description']))
                else:
                    lec_desc.append('')
            lecture['title'] = lec_title
            lecture['description'] = lec_desc
            sections_desc.append(lecture)
        return sections_desc
    else:
        print('Wrong option!')
        exit()

def extract_text_in_courses(courses):
    new_courses = list()
    for k in courses.keys():
        if k != '':
            dict_course = dict()
            title = extract_title_in_course(course=courses[k])
            sections = extract_section_in_course(course=courses[k], option='section')  # extract the title of a section
            sections_desc = extract_section_in_course(course=courses[k], option='section_desc')  # extract the content of a section 
            dict_course['course_id'] = k
            dict_course['course_title'] = title
            dict_course['sections'] = sections
            dict_course['sections_desc'] = sections_desc
            new_courses.append(dict_course)
    return new_courses