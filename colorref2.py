from graph_io import load_graph

"""
colorref by Rudolfs
"""
def color_refinement(graphs):

    global_neighborhood_to_color = {}  # neighbourhood -> colour

    colorings = {}  # graph -> colouring

    # assing initial colouring (= 0) for all vertices
    previous_colourings = {graph: {v: 0 for v in graph.vertices}
                           for graph in graphs}  # graph -> colouring

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

        # create unique signature for color count combination
        partition_signature = tuple(sorted(partitions.items()))
        # add signature and corresponding graph to others
        all_partitions.setdefault(partition_signature, []).append(idx)

    result = [(eq_class, iterations[eq_class[0]], all(count == 1 for _, count in part))
              for part, eq_class in all_partitions.items()]
    return result


def basic_colorref(path):
    with open(path) as f:
        L = load_graph(f, read_list=True)

    graphs = L[0]

    colouring, iterations = color_refinement(graphs)
    result = partition(graphs, colouring, iterations)

    return result

