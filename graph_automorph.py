from graph_io import load_graph
from graph import Graph
import time


def color_refinement(graphs, coloring_init):
    next_color = max(max(coloring_init[graph][v]
                     for v in graph.vertices) for graph in graphs) + 1

    coloring = coloring_init.copy()
    refined = True
    neighbourhood_map = {}

    while refined:
        refined = False

        for graph in graphs:
            coloring_new = {}

            for v in graph.vertices:
                neighborhood_colors = tuple(
                    sorted(coloring[graph][neighbor] for neighbor in v.neighbours))

                # use both the neighbourhood and the current vertex color to determine the new color
                key = (neighborhood_colors, coloring[graph][v]) 
                color = neighbourhood_map.get(key)
                if color is None:
                    neighbourhood_map[key] = next_color
                    next_color += 1
                coloring_new[v] = neighbourhood_map[key]

            if (len(set(coloring_new.values())) != len(set(coloring[graph].values()))):
                refined = True
            
            coloring[graph] = coloring_new
        
    return coloring


def partition(graphs, coloring):
    partitions = {}
    for graph in graphs:
        vert_colors = sorted(coloring[graph].values())
        partitions.setdefault(tuple(vert_colors), []).append(graph)

    eq_classes = []
    for col, gr in partitions.items():
        eq_classes.append((gr, len(set(col)) == len(col)))
    return eq_classes


def count_isomorphism(D, I, G, H, coloring, depth=0):
    # new_coloring = {g: {v: coloring[g][v] for v in g.vertices} for g in [G, H]}
    new_coloring = color_refinement([G, H], coloring)

    g_colors = sorted([new_coloring[G][v] for v in G.vertices])
    h_colors = sorted([new_coloring[H][v] for v in H.vertices])
    balanced = g_colors == h_colors
    bijection = len(g_colors) == len(set(h_colors))
    
    if not balanced:
        return 0

    if bijection:
        return 1

    
    next_color = max(h_colors) + 1
    # find a color with more than one vertex in G
    for i in range(1, len(g_colors)):
        if g_colors[i] == g_colors[i - 1]:
            color = g_colors[i]
            break

    x = None
    for v in G.vertices:
        if new_coloring[G][v] == color and v not in D:
            x = v
            break
    
    num = 0
    for v in H.vertices:
        if new_coloring[G][v] == color and v not in I:
            # test_coloring = {g: {v: new_coloring[g][v] for v in g.vertices} for g in [G, H]}
            new_coloring[H][v] = next_color
            new_coloring[G][x] = next_color
            d1 = D[:]
            d1.append(x)
            i1 = I[:]
            i1.append(v)
            num += count_isomorphism(d1, i1, G, H, new_coloring, depth + 1)
    return num
            


def find_isomorphisms(graphs, coloring, all_graphs):
    isomorphic_pairs = []

    for i in range(len(graphs)):
        for j in range(i + 1, len(graphs)):
            D, I = [], []
            print(f'G = {all_graphs.index(graphs[i])}, H = {all_graphs.index(graphs[j])}')
            count = count_isomorphism(D, I, graphs[i], graphs[j], coloring)
            if count > 0: isomorphic_pairs.append((graphs[i], graphs[j]))
    
    return isomorphic_pairs
                

def classify(path):
    with open(path) as f:
        graphs = load_graph(f, read_list=True)[0]

    initial_coloring = {graph: {v: 0 for v in graph.vertices}
                        for graph in graphs}

    coloring = color_refinement(graphs, initial_coloring)
    eq_classes = partition(graphs, coloring)
    # print(eq_classes)

    # for testing a single pair
    print(count_isomorphism([], [], graphs[1], graphs[1], coloring))
    
    # isomorphisms = []
    # for cl in eq_classes:
    #     if not cl[1]:
    #         print(f'Checking set: {[graphs.index(i) for i in cl[0]]}')
    #         pairs = find_isomorphisms(cl[0], coloring, graphs)
    #         isomorphisms.extend(pairs)
   
    #     else:
    #         isomorphisms.append(tuple(cl[0]))

    
    # for pair in isomorphisms:
    #     print('---------------', [graphs.index(g) for g in pair], '---------------')


if __name__ == '__main__':
    start_time = time.time()
    classify('SampleGraphSetBranching/torus72.grl')
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
        
