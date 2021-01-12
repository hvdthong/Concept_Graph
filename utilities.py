def read_file(path):
    data = list()
    with open(path) as f:
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

def filtering_concept(data):
    new_concept = list()
    for i in range(1, len(data)):
        d = data[i].split('\t')
        concept, alias = d[0], d[1]
        if len(alias) > 0:
            concept = clean_concept(concept) + ',' + clean_alias(alias)
        elif 'Natural Language Processing' in concept:
            concept = clean_concept(concept) + ',' + 'NLP'
        else:
            concept = clean_concept(concept)
        concept = [c.lower().strip() for c in concept.split(',')]
        concept = ','.join(list(set(concept)))        
        new_concept.append(concept)
    return new_concept