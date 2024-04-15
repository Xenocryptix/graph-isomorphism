from collections import Counter
from graph import *
from graph_io import *
import copy

with open('SampleGraphSetBranching/torus24.grl') as f:
    L_list = load_graph(f,read_list=True)
L = L_list[0]

def uniform_coloring(L):
    for G in L:
        for v in G.vertices:
            v.label = 0
    return L

def initial_coloring(L):
    for G in L:
        for v in G.vertices:
            v.label = v.degree
    return L

def color_refinement(L):
    color = []
    next_color = 0
    for G in L:
        next_color = max([v.label for v in G.vertices])
        color.append(set([v.label for v in G.vertices]))
    
    prev_len = [0] * len(L)
    next_color += 1

    while prev_len != [len(c) for c in color]:
        prev_len = [len(c) for c in color]
        color_map = dict()
        for G in L:
            i = L.index(G)
            new_color = dict()
            for v in G.vertices:
                neighbor_colors = tuple(sorted([v.label for v in v.neighbours]))
                if neighbor_colors not in color_map:
                    color_map[neighbor_colors] = next_color
                    next_color += 1
                new_color[v] = color_map[neighbor_colors]
            for v in G.vertices:
                v.label = new_color[v]
            color[i] = set([v.label for v in G.vertices])
    return L
    
def print_result(L):
    for G in L:
        print(sorted([v.label for v in G.vertices]))

def grouping(L):
    graph_dict = dict()
    for G in L:
        i = L.index(G)
        col = sorted([v.label for v in G.vertices])
        if (str(col) not in graph_dict):
            graph_dict[str(col)] = []
        graph_dict[str(col)].append(i)
    result = list(graph_dict.values())
    print(result)
    return result

def get_class(L):
    color = {}
    for G in L:
        for v in G.vertices:
            if v.label not in color.keys():
                color[v.label] = 1
            else:
                color[v.label] += 1
                if color[v.label] >= 4:
                    return v.label

def count_isomorphism(g: Graph, h: Graph, d: list[Vertex] = [], i: list[Vertex] = []) -> int:
    ref = color_refinement([g, h])
    g_color = sorted([v.label for v in g.vertices])
    h_color = sorted([v.label for v in h.vertices])
    if g_color != h_color: #unbalanced    
        return 0
    elif len(g_color) == len(set(h_color)): #bijective
        return 1
    
    c = get_class([g, h])
    next_color = max(g_color) + 1

    for v in g:
        if v.label == c and v not in d:
            x = v
            break
    num = 0
    for v in h:
        if v.label == c and v not in i:
            g1 = copy.deepcopy(g)
            h1 = copy.deepcopy(h)
            g1.vertices[g.vertices.index(x)].label = next_color
            h1.vertices[h.vertices.index(v)].label = next_color
            d1 = d[::]
            i1 = i[::]
            d1.append(x)
            i1.append(v)
            num += count_isomorphism(g1, h1, d1, i1)
    return num

def count_isomorphism_2(G_x, G_y):
    #For counting automorphisms, G_x == G_y 
    x_color = sorted([v.label for v in G_x.vertices])
    y_color = sorted([v.label for v in G_y.vertices])
    if x_color != y_color: #unbalanced    
        return 0
    elif len(x_color) == len(set(x_color)): #bijective
        return 1
    
    graph_x = copy.deepcopy(G_x)
    graph_y = copy.deepcopy(G_y)
    v_x = {}
    v_y = {}
    for v in graph_x.vertices:
        v_x.setdefault(v.label, []).append(v)
    for v in graph_y.vertices:
        v_y.setdefault(v.label, []).append(v)
    next_color = max(x_color) + 1
    num = 0
    for v in v_x:
        x_col = v_x[v]
        y_col = v_y[v]
        if len(x_col) < 2:
            continue
        for x in x_col:
            for y in y_col:
                tmp = x.label
                x.label = next_color
                y.label = next_color
                ref = color_refinement([graph_x, graph_y]) 
                ref_x = ref[0]
                ref_y = ref[1]
                x.label = tmp
                y.label = tmp
                num += count_isomorphism(ref_x, ref_y)
                #Revert coloring
        return num

initial_coloring(L)
color_refinement(L)
# grouping(L)   

# uniform_coloring(L)
a = count_isomorphism(L[0], L[0])
print(a)


# For #Aut problem, group the graphs on their number of automorphisms            