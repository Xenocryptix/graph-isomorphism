from collections import Counter
from graph import *
from graph_io import *
import copy
# from color_refinement import color_refinement

with open('SampleGraphSetBranching/products216.grl') as f:
    L_list = load_graph(f,read_list=True)
L = L_list[0]

def uniform_coloring(L):
    for G in L:
        for v in G.vertices:
            v.colornum = 0
    return L

def initial_coloring(L):
    for G in L:
        for v in G.vertices:
            v.colornum = v.degree
    return L

def check_neighbours(v1, v2):
    if len(v1.neighbours) == len(v2.neighbours):
        n1 = sorted(list(v.colornum for v in v1.neighbours))
        n2 = sorted(list(v.colornum for v in v2.neighbours))
        return n1 == n2
    return False

def color_refinement(L):
    vertices = list()
    for G in L:
        for v in G.vertices:
            vertices.append(v)

    change = True
    while change:
        change = False
        color_map = dict()
        for v in vertices:
            if v.colornum not in color_map.keys():
                color_map[v.colornum] = set()
            color_map[v.colornum].add(v)
        
        color_changes = dict()
        for same_color in color_map.values():
            new_colors = dict()
            for v in same_color:
                added = False
                for vertices_list in new_colors.values():
                    if check_neighbours(v, vertices_list[0]):
                        vertices_list.append(v)
                        added = True
                        break
                if not added:
                    new_colors[len(new_colors.keys())] = [v]
                if len(new_colors.keys()) > 1:
                    change = True
            for vertices_list in new_colors.values():
                color_changes[len(color_changes.keys())] = vertices_list
        for color, vertices_list in color_changes.items():
            for v in vertices_list:
                v.colornum = color
    
def print_result(L):
    for G in L:
        print(sorted([v.colornum for v in G.vertices]))

def grouping(L):
    graph_dict = dict()
    for G in L:
        i = L.index(G)
        col = sorted([v.colornum for v in G.vertices])
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
            if v.colornum not in color.keys():
                color[v.colornum] = 1
            else:
                color[v.colornum] += 1
                if color[v.colornum] >= 4:
                    return v.colornum

def count_isomorphism(g: Graph, h: Graph, d: list[Vertex] = [], i: list[Vertex] = []) -> int:
    ref = color_refinement([g, h])
    g_color = sorted([v.colornum for v in g.vertices])
    h_color = sorted([v.colornum for v in h.vertices])
    if g_color != h_color: #unbalanced    
        return 0
    elif len(g_color) == len(set(h_color)): #bijective
        return 1
    
    c = get_class([g, h])
    next_color = max(g_color) + 1

    for v in g:
        if v.colornum == c and v not in d:
            x = v
            break
    num = 0
    for v in h:
        if v.colornum == c and v not in i:
            g1 = Graph(False) + g
            h1 = Graph(False) + h
            g1.vertices[g.vertices.index(x)].colornum = next_color
            h1.vertices[h.vertices.index(v)].colornum = next_color
            d1 = d[::]
            i1 = i[::]
            d1.append(x)
            i1.append(v)
            num += count_isomorphism(g1, h1, d1, i1)
    return num


initial_coloring(L)
color_refinement(L)
# grouping(L)   
# uniform_coloring(L)
# print(count_isomorphism(L[0], L[0]))

for i in range(len(L)):
    for j in range(len(L)):
        if i < j:
            number = count_isomorphism(L[i] + Graph(False), L[j] + Graph(False))
            if number > 0:
                print(f"Found {number} isomorphisms between graphs {i} and {j}\n")        