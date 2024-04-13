from graph_io import load_graph


def color_refinement(graphs, coloring):
    global_neighborhood_to_color = {}  # neighbourhood -> colour
    colorings = {}  # graphs -> graph -> vertex -> color
    previous_colourings = coloring

    iterations = {graphs.index(graph): 0 for graph in graphs}
    converged_graphs = set()

    while len(converged_graphs) < len(graphs):
        for graph in graphs:
            if graph in converged_graphs:
                continue

            neighborhood_to_color, coloring = {}, {}
            for vertex in graph.vertices:
                # neighbour colours of vertex, sorted and stored as a tuple
                neighborhood_colors = sorted(
                    previous_colourings[graph][neighbor] for neighbor in vertex.neighbours)
                neighborhood = tuple(neighborhood_colors)

                color = neighborhood_to_color.get(neighborhood)
                if color is None:
                    # try to get the colour from the global mapping
                    # otherwise create colour and assign it to neighbourhood signature globaly
                    color = global_neighborhood_to_color.get(
                        neighborhood, len(global_neighborhood_to_color) + 1)
                    global_neighborhood_to_color.setdefault(
                        neighborhood, color)

                    neighborhood_to_color[neighborhood] = color

                coloring[vertex] = color

            # check if new colouring creates new colours from previous iteration
            refined = len(set(coloring.values())) > len(
                set(previous_colourings[graph].values()))

            if not refined:
                converged_graphs.add(graph)
            else:
                iterations[graphs.index(graph)] += 1

            previous_colourings[graph] = coloring
            colorings[graph] = coloring

    return colorings, iterations


def partition(graphs, colouring, iterations):
    all_partitions = {}  # partition -> equivelance classes (lists of graphs)
    for idx, graph in enumerate(graphs):
        # count each colour
        partitions = {colour: 0 for colour in colouring[graph].values()}
        for v in graph.vertices:
            partitions[colouring[graph][v]] += 1

        partition_signature = tuple(sorted(partitions.items()))
        all_partitions.setdefault(partition_signature, []).append(idx)

    # (eq_class, # of iterations, is_discrete)
    result = [(eq_class, iterations[eq_class[0]], all(count == 1 for _, count in part))
              for part, eq_class in all_partitions.items()]
    return result


def count_isomorphism(D, I, G, H, coloring, depth=0):
    # Log the depth and the state of D and I for diagnostics.
    print(f"Recursion depth: {depth}, D: {D}, I: {I}")

    alpha = color_refinement([G, H], coloring)[0]
    
    coloured_G = sorted([alpha[G][v] for v in G.vertices])
    coloured_H = sorted([alpha[H][v] for v in H.vertices])

    balanced = coloured_G == coloured_H
    bijection = len(coloured_G) == len(set(coloured_G))

    if not balanced: return 0
    if bijection: return 1

    C = find_color_class(coloured_G)
    num_isomorphisms = 0

    for v in G.vertices:
        if alpha[G][v] == C:
            for w in H.vertices:
                if alpha[H][w] == C:
                    new_color = max(coloured_G) + 1

                    start_coloring = alpha.copy()
                    D.append(v)
                    I.append(w)
                    start_coloring[G][v] = new_color
                    start_coloring[H][w] = new_color
                    for g in [G, H]:
                        for vert in g.vertices:
                            if vert not in D and vert not in I:
                                start_coloring[g][vert] = 0

                    if depth > 10: return 0
                    num = count_isomorphism(D, I, G, H, start_coloring, depth=depth+1)                    
                    num_isomorphisms += num
                
    return num_isomorphisms


def find_color_class(col_list):
    # Helper function to select a color class C with |C| ≥ 4 from the coloring
    # Since we know that both graphs are balanced (coloured_G == coloured_H), and
    # this list is sorted, we look for adjacent duplicates

    for i in range(1, len(col_list)):
        if col_list[i] == col_list[i - 1]:
            return col_list[i]
    return None


def isomorphism_check(graphs, coloring):
    # Main function to check isomorphism between all pairs in a set of graphs.
    isomorphic_graphs = []
    for i, G in enumerate(graphs):
        for j, H in enumerate(graphs):
            if i < j:  # Avoid checking the same pair twice or a graph with itself
                D, I = [], []
                print(count_isomorphism(D, I, G, H, coloring))
                return

    return isomorphic_graphs


def basic_colorref(path):
    with open(path) as f:
        graphs = load_graph(f, read_list=True)[0]

    initial_coloring = {graph: {v: 0 for v in graph.vertices}
                        for graph in graphs}  # graphs -> graph -> vertex -> color

    coloring, iterations = color_refinement(graphs, initial_coloring)
    part = partition(graphs, coloring, iterations)

    for eq_class in part:
        if not eq_class[2]:
            gr = [graphs[i] for i in eq_class[0]]
            isomorphism_check(gr, coloring)
            


if __name__ == '__main__':
    basic_colorref(
        'SampleGraphSetBranching/torus24.grl')
