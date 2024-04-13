from collections import Counter
from graph import *
from graph_io import *
import time

with open('SampleGraphSetBranching/torus24.grl') as f:
    L = load_graph(f,read_list=True)

def initial_coloring(L):
    for G in L[0]:
        for v in G.vertices:
            v.label = v.degree
    return L

def color_refinement(L):
    color = []
    next_color = 0
    for G in L[0]:
        next_color = max([v.label for v in G.vertices])
        color.append(set([v.label for v in G.vertices]))
    
    prev_len = [0] * len(L[0])
    next_color += 1
    iter = [1] * len(L[0])

    while prev_len != [len(c) for c in color]:
        prev_len = [len(c) for c in color]
        color_map = dict()
        for G in L[0]:
            i = L[0].index(G)
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
            if (prev_len[i] != len(color[i])):
                iter[i] += 1
    
def print_result(L):
    for G in L[0]:
        print(sorted([v.label for v in G.vertices]))

def grouping(L):
    graph_dict = dict()
    for G in L[0]:
        i = L[0].index(G)
        col = sorted([v.label for v in G.vertices])
        if (str(col) not in graph_dict):
            graph_dict[str(col)] = []
        graph_dict[str(col)].append(i)
    result = list(graph_dict.values())
    print(result)
    return result

def count_isomorphism(G_x, G_y):
    #For counting automorphisms, G_x == G_y 
    x_color = sorted([v.label for v in G_x.vertices])
    y_color = sorted([v.label for v in G_y.vertices])
    if x_color != y_color: #unbalanced    
        return 0
    elif len(v_x) == len(set(v_x)): #bijective
        return 1
    
    graph_x = G_x.copy()
    graph_y = G_y.copy()
    v_x = {}
    v_y = {}
    for v in graph_x.vertices:
        v_x[v.label].append(v)
    for v in graph_y.vertices:
        v_y[v.label].append(v)
    next_color = max([v.label for v in graph_x.vertices]) + 1
    num = 0
    for v in v_x:
        x_color = v_x[v]
        y_color = v_y[v]
        if len(x_color) < 2:
            continue
        for x in x_color:
            for y in y_color:
                x.label, y.label = next_color
                color_refinement([graph_x, graph_y]) 
                #TODO: the above line is pseudocode, the function might need to return a value which is assigned to both graphs
                num += count_isomorphism(graph_x, graph_y)


initial_coloring(L)
color_refinement(L)
grouping(L)

# print_result(L)    

# For #Aut problem, group the graphs on their number of automorphisms            