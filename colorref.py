from graph import *
from graph_io import *
import time

def basic_colorref(path):
    with open(path) as f:
        L = load_graph(f,read_list=True)
    
    color = []
    next_color = 0
    for G in L[0]:
        for v in G.vertices:
            v.label = v.degree
            next_color = max(next_color, v.label)
        color.append(set([v.label for v in G.vertices]))

    prev_len = [0] * len(L[0])
    next_color += 1
    iter = [1] * len(L[0])

    while prev_len != [len(c) for c in color]:
        prev_len = [len(c) for c in color]
        change = [0] * len(L[0])
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

    graph_dict = dict()
    for G in L[0]:
        i = L[0].index(G)
        col = sorted([v.label for v in G.vertices])
        if (str(col) not in graph_dict):
            graph_dict[str(col)] = tuple([[], iter[i], len(col) == len(set(col))])
        graph_dict[str(col)][0].append(i)
    result = list(graph_dict.values())
    print(result)
    return result

if __name__ == '__main__':
    time1 = time.time_ns()
    basic_colorref('SampleGraphsBasicColorRefinement/colorref_smallexample_6_15.grl')
