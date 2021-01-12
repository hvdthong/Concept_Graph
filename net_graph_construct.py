import pandas as pd 

def create_dictionary_edges(data):
    root_dict = dict()
    for d in data:
        if d[0] not in root_dict.keys():
            root_dict[d[0]] = {}
        
        if d[1] not in root_dict[d[0]].keys():
            root_dict[d[0]][d[1]] = float(d[2])
    return root_dict

def net_weight_cover_edges(edges, threshold):
    dict_cover_edges = create_dictionary_edges(edges)
    edges = list()
    for root in dict_cover_edges.keys():
        for dest in dict_cover_edges[root].keys():
            root_to_dest = dict_cover_edges[root][dest]
            dest_to_root = None
            if dest in dict_cover_edges.keys() and root in dict_cover_edges[dest].keys():
                dest_to_root = dict_cover_edges[dest][root]
            
            if dest_to_root == None:
                if root_to_dest >= threshold:
                    edge = list()
                    edge.append(root)
                    edge.append(dest)
                    edge.append(root_to_dest)
                    edges.append(edge)
            else:
                if root_to_dest > dest_to_root and (root_to_dest - dest_to_root) >= threshold:
                    edge = list()
                    edge.append(root)
                    edge.append(dest)
                    edge.append(root_to_dest - dest_to_root)
                    edges.append(edge)
                elif root_to_dest < dest_to_root and (dest_to_root - root_to_dest) >= threshold:
                    edge = list()
                    edge.append(dest)
                    edge.append(root)
                    edge.append(dest_to_root - root_to_dest)
                    edges.append(edge)
    return edges

def top_initial_outdegree_nodes(edges, top=10):
    root_node, dest_node, weight = list(), list(), list()
    for e in edges:
        root_node.append(e[0])
        dest_node.append(e[1])
        weight.append(float(e[2]))
    df = pd.DataFrame({'root': root_node, 'dest': dest_node, 'weight': weight})
    df = df.groupby(['root'])['weight'].sum().reset_index(name='weight').sort_values(['weight'], ascending=False).head(top)['root']
    return list(df)

def net_weight_order_edges(edges, threshold):
    dict_order_edges = create_dictionary_edges(edges)
    top_nodes = top_initial_outdegree_nodes(edges=edges, top=10)
        
    while (True):
        new_added_nodes = list()
        for root in top_nodes:
            for dest in dict_order_edges[root].keys():
                root_to_dest = dict_order_edges[root][dest]
                dest_to_root = None
                
                if dest in dict_order_edges.keys() and root in dict_order_edges[dest].keys():
                    dest_to_root = dict_order_edges[dest][root]

                if dest_to_root == None:
                    if root_to_dest >= threshold:
                        if dest not in new_added_nodes and dest not in top_nodes:
                            new_added_nodes.append(dest)
                else:                    
                    if root_to_dest < dest_to_root and (dest_to_root - root_to_dest) >= threshold:
                        if dest not in new_added_nodes and dest not in top_nodes:
                            new_added_nodes.append(dest)
                        
        if len(new_added_nodes) == 0:
            break
        else:
            top_nodes += new_added_nodes
 
    edges = list()
    for root in top_nodes:
        for dest in dict_order_edges[root].keys():
            root_to_dest = dict_order_edges[root][dest]
            dest_to_root = None
            if dest in dict_order_edges.keys() and root in dict_order_edges[dest].keys():
                dest_to_root = dict_order_edges[dest][root]
            
            if dest_to_root == None:
                if root_to_dest >= threshold:
                    edge = list()
                    edge.append(root)
                    edge.append(dest)
                    edge.append(root_to_dest)
                    edges.append(edge)
            else:
                if root_to_dest > dest_to_root and (root_to_dest - dest_to_root) >= threshold:
                    edge = list()
                    edge.append(root)
                    edge.append(dest)
                    edge.append(root_to_dest - dest_to_root)
                    edges.append(edge)
                elif root_to_dest < dest_to_root and (dest_to_root - root_to_dest) >= threshold:
                    edge = list()
                    edge.append(dest)
                    edge.append(root)
                    edge.append(dest_to_root - root_to_dest)
                    edges.append(edge)
    return edges     