from graph_io import load_graph


def color_refinement(graphs, coloring_init):
    next_color = max(max(coloring_init[graph][v]
                     for v in graph.vertices) for graph in graphs) + 1

    coloring = coloring_init.copy() # copy needed here?
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

            coloring[graph] = coloring_new # copy needed here?
        
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
    g_colors = sorted([coloring[G][v] for v in G.vertices])
    h_colors = sorted([coloring[H][v] for v in H.vertices])


    # Debug print statements
    # print()
    # print('Depth: ', depth)
    # print('G col: ', g_colors)
    # print('H col: ', h_colors)
    # print('Balanced: ',g_colors == h_colors)
    # print('Bijection: ',len(g_colors) == len(set(g_colors)))


    if g_colors != h_colors:
        return 0
    if len(g_colors) == len(set(g_colors)):
        return 1

    C_G, C_H = {}, {}
    for v in G.vertices:
        C_G.setdefault(coloring[G][v], []).append(v)
    for v in H.vertices:
        C_H.setdefault(coloring[H][v], []).append(v)

    next_color = max(g_colors) + 1

    num = 0
    i = 0
    for color in C_G:
        if len(C_G[color]) < 2:
            continue
        
        # Debug
        # print('Chosen color: ', color)
        
        for v in C_G[color]:
            if v in D: continue # adding this speeds it up a lot
            for w in C_H[color]:
                if w in I: continue # this too
                start_coloring = {G: {}, H: {}}
                
                for g in [G, H]:
                    for u in g.vertices:
                        if u not in D and u not in I:
                            start_coloring[g][u] = 0
                        else:
                            start_coloring[g][u] = coloring[g][u]
                
                start_coloring[G][v] = next_color
                start_coloring[H][w] = next_color
                D.append(v)
                I.append(w)

                alpha = color_refinement([G, H], start_coloring.copy())

                num += count_isomorphism(D, I, G, H, alpha, depth + 1) # should alpha be copied?
                
                if num > 0: return num # return as soon as we find an isomorphism

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

    # for testing a single pair
    # print(count_isomorphism([], [], graphs[0], graphs[5], coloring))
    
    for cl in eq_classes:
        if not cl[1]:
            print(f'Checking set: {[graphs.index(i) for i in cl[0]]}')
            pairs = find_isomorphisms(cl[0], initial_coloring, graphs)
            print()
            print()
            for p in pairs: 
                print('---------------', graphs.index(p[0]), graphs.index(p[1]), '---------------')



if __name__ == '__main__':
    classify(
        'SampleGraphSetBranching/torus144.grl')
