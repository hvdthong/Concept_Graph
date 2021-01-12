def name_node(node):
    return node.split(',')[0]

def json_node(edges):
    nodes = list()
    for e in edges:
        nodes.append(e[0])
        nodes.append(e[1])
    nodes = list(set(nodes))
    nodes = list(sorted([name_node(n) for n in nodes]))
    
    new_nodes = list()
    for i in range(0, len(nodes)):
        node = {}
        node['name'] = nodes[i]        
        node['id'] = i + 1
        new_nodes.append(node)
    return new_nodes

def json_links(edges):
    nodes = list()
    for e in edges:
        nodes.append(e[0])
        nodes.append(e[1])
    nodes = list(set(nodes))
    nodes = list(sorted(nodes))
    
    new_edges = list()
    for e in edges:
        index_source = nodes.index(e[0]) + 1
        index_target = nodes.index(e[1]) + 1
        weight = str(round(e[2], 2))
        
        edge = {}
        edge['source'] = index_source
        edge['target'] = index_target
        edge['type'] = weight
        new_edges.append(edge)
    return new_edges