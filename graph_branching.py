from collections import Counter
from graph import *
from graph_io import *
import time

with open('SampleGraphsBasicColorRefinement/colorref_smallexample_6_15.grl') as f:
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
    

initial_coloring(L)
color_refinement(L)
grouping(L)

# print_result(L)                