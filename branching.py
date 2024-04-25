from colorref import colorref
from graph import Graph, Vertex, Edge


def count_isomorphisms(d, i, g, h, coloring, count_mode=False):
    """
    Counts or checks the existence of isomorphisms between two graphs 
    with sets of already distinguished vertices.
    Parameters:
        D (list): List of distinguished vertices in G.
        I (list): List of distinguished vertices in H.
        G (Graph): The first graph.
        H (Graph): The second graph.
        coloring (dict): Coloring dictionary for graphs.
        count_mode (bool): If True, count all isomorphisms; otherwise, check if isomorphic only.
    Returns:
        int or bool: Number of isomorphisms or isomorphic flag.
    """
    coloring = colorref([g, h], coloring)

    g_colors = sorted([coloring[g][v] for v in g.vertices])
    h_colors = sorted([coloring[h][v] for v in h.vertices])

    if g_colors != h_colors:
        return 0 if count_mode else False
    if len(g_colors) == len(set(g_colors)):
        return 1 if count_mode else True

    # We know that g_colors is sorted and equal to h_colors,
    # so a repeated color means a color class with >= 4 vertices
    for idx in range(1, len(g_colors)):
        if g_colors[idx] == g_colors[idx - 1]:
            color = g_colors[idx]
            break

    next_color = max(g_colors + h_colors) + 1

    for vert in g:
        if coloring[g][vert] == color and vert not in d:
            vert_g = vert
            break

    num = 0
    for vert in h:
        if coloring[h][vert] == color and vert not in i:
            vert_h = vert

            # Deep copy of coloring
            new_coloring = {graph: dict(coloring[graph]) for graph in [g, h]}

            # Change the coloring by coloring the two selected vertices the same (distinct) color
            new_coloring[g][vert_g] = next_color
            new_coloring[h][vert_h] = next_color

            count = count_isomorphisms(
                d + [vert_g], i + [vert_h], g, h, new_coloring, count_mode)

            # Differentiate based on count_mode
            if count_mode:
                num += count
            elif count:
                return True

    return num if count_mode else False


def duplicate_graph(graph):
    """
    Creates a duplicate of the given graph with seperate (identic) vertices and edges.
    Parameters:
        graph (Graph): The graph to duplicate.
    Returns:
        Graph: A new graph object that is a duplicate of the given graph.
    """
    new_graph = Graph(False)
    verts = {}
    for vert in graph.vertices:
        new_vert = Vertex(new_graph, vert.label)

        verts[vert] = new_vert
        new_graph.add_vertex(new_vert)

    for edge in graph.edges:
        tail = edge.tail
        head = edge.head
        new_edge = Edge(verts.get(tail), verts.get(head))
        new_graph.add_edge(new_edge)

    return new_graph


def automorphisms(graph):
    """
    Counts the number of automorphisms of a graph.
    Parameters:
        graph (Graph): The graph to analyze.
    Returns:
        int: The number of automorphisms.
    """
    copy = duplicate_graph(graph)
    coloring = {graph: {v: 0 for v in graph.vertices}
                for graph in [graph, copy]}

    return count_isomorphisms([], [], graph, copy, coloring, True)


def group_isomorphic(graphs):
    """
    Groups graphs that are isomorphic to each other based on the provided coloring.
    Parameters:
        graphs (list): A list of graph objects.
        coloring (dict): A coloring used to help determine isomorphisms.
    Returns:
        list: A list of lists, where each sublist contains indices of isomorphic graphs.
    """
    coloring = {graph: {vert: 0 for vert in graph.vertices}
                for graph in graphs}
    groups = []
    for i, g in enumerate(graphs):
        found = False
        for group in groups:
            is_isomorphic = count_isomorphisms(
                [], [], graphs[group[0]], g, coloring, False)
            if is_isomorphic:
                group.append(i)
                found = True
        if not found:
            groups.append([i])

    return groups
