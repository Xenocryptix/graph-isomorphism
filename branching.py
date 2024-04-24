from colorref import colorref, partition
from graph import Graph, Vertex, Edge


def count_isomorphisms(D, I, G, H, coloring, count_mode=False):
    coloring = colorref([G, H], coloring)

    g_colors = sorted([coloring[G][v] for v in G.vertices])
    h_colors = sorted([coloring[H][v] for v in H.vertices])

    if g_colors != h_colors:
        return 0 if count_mode else False
    if len(g_colors) == len(set(g_colors)):
        return 1 if count_mode else True

    for i in range(1, len(g_colors)):
        if g_colors[i] == g_colors[i - 1]:
            C = g_colors[i]
            break

    next_color = max(max(coloring[G].values()), max(coloring[H].values())) + 1

    for vert in G:
        if coloring[G][vert] == C and vert not in D:
            vert_g = vert
            break

    num = 0
    for vert in H:
        if coloring[H][vert] == C and vert not in I:
            vert_h = vert

            new_coloring = {graph: dict(coloring[graph]) for graph in [G, H]}

            new_coloring[G][vert_g] = next_color
            new_coloring[H][vert_h] = next_color

            count = count_isomorphisms(
                D + [vert_g], I + [vert_h], G, H, new_coloring, count_mode)
            if count_mode:
                num += count
            elif count:
                return True

    return num if count_mode else False


def duplicate_graph(graph):
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


def automorphisms(graph, coloring):
    copy = duplicate_graph(graph)
    coloring = {graph: {v: 0 for v in graph.vertices}
                for graph in [graph, copy]}

    count = count_isomorphisms(
        [], [], graph, copy, coloring, True)
    return count


def find_isomorphisms(graphs, coloring):
    isomorphic_pairs = []

    for i in range(len(graphs)):
        for j in range(i + 1, len(graphs)):
            isomorphic = count_isomorphisms(
                [], [], graphs[i], graphs[j], coloring, False)
            if isomorphic:
                isomorphic_pairs.append((graphs[i], graphs[j]))

    return isomorphic_pairs