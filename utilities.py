def read_file(path):
    data = list()
    with open(path, encoding='utf-8') as f:
        for line in f:
            data.append(line.strip())
    return data

def clean_concept(word):
    word = word.replace('_', ' ')
    if '(' in word:
        index = word.find('(')
        return word[:index].strip()
    else:
        return word.strip()

def clean_alias(word):
    if word == 'YOLO___yolo____Yolo____YOLO (Algorithm)':
        return 'yolo, yolo algorithm'
    
    word = word.replace('____', ',')
    word = word.replace('___', ',')
    word = word.replace('__', ',')
    word = word.replace('_', ' ')
    if '(' in word:
        return word[:word.find('(')].strip() + ',' + word[(word.find('(') + 1):word.find(')')].strip()
    else:
        return word.strip()

def max_concept_length(concept):
    return max([len(c.split()) for c in concept.split(',')])

def filtering_concept(data):    
    new_concept = dict()
    for i in range(1, len(data)):
        d = data[i].split('\t')
        if len(d) > 1:
            concept, alias = d[0], d[1]            
            if len(alias) > 0:
                concept = clean_concept(concept) + ',' + clean_alias(alias)
            elif 'Natural Language Processing' in concept:
                concept = clean_concept(concept) + ',' + 'NLP'
            else:
                concept = clean_concept(concept)

            concept = [c.lower().strip() for c in concept.split(',')]
            concept = ','.join(list(set(concept)))            
            new_concept[concept] = max_concept_length(concept)        
    new_concept = dict(sorted(new_concept.items(), key=lambda item: item[1], reverse=True))
    new_concept = list(new_concept.keys())
    return new_concept