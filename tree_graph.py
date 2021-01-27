def create_dictionary_edges(data):
    root_dict = dict()
    for d in data:
        if d[0] not in root_dict.keys():
            root_dict[d[0]] = {}
        
        if d[1] not in root_dict[d[0]].keys():
            root_dict[d[0]][d[1]] = float(d[2])
    return root_dict

def extract_nodes(edges):
    nodes = list()
    for e in edges:
        nodes.append(e[0])
        nodes.append(e[1])
    nodes = list(sorted(set(nodes)))
    return nodes

def checking_concept(concept, nodes):
    concept = concept.lower()
    flag = False
    for node in nodes:
        split_node = node.split(',')
        if concept in split_node:
            return True, node
    return flag, concept

def tree_concept(concept, edges):
    dict_order_edges = create_dictionary_edges(edges)
    root_nodes = [concept]
    tree_nodes = dict()
    while (True):
        flag = len(root_nodes)
        for root_node in root_nodes:
            if root_node not in tree_nodes and root_node in dict_order_edges.keys():
                tree_nodes[root_node] = dict_order_edges[root_node].keys()
                dest_nodes = dict_order_edges[root_node].keys()
                for dest_node in dest_nodes:
                    if dest_node not in root_nodes:
                        root_nodes.append(dest_node)                       
        if flag == len(root_nodes):
            break
    
    draw_edges = list()
    for root in tree_nodes.keys():
        dest_nodes = tree_nodes[root]
        for dest in dest_nodes:
            for e in edges:
                draw_edge = list()
                if e[0] == root and e[1] == dest:
                    draw_edge.append(e[0])
                    draw_edge.append(e[1])
                    draw_edge.append(e[2])
                    if draw_edge not in draw_edges:
                        draw_edges.append(draw_edge)    
    return draw_edges