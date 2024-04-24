from graph_io import load_graph
from graph import Graph, Vertex, Edge

def colorref(graphs, coloring):
    vertices = [vert for graph in graphs for vert in graph.vertices]

    new_coloring = {graph: dict(coloring[graph]) for graph in graphs}

    refined = True
    while refined:
        refined = False

        color_classes = {}
        for v in vertices:
            color = new_coloring[v.graph][v]
            color_classes.setdefault(color, []).append(v)

        color_changes = {}
        
        for color, same_col_verts in color_classes.items():
            new_colors = {}
            for v in same_col_verts:
                added = False

                for verts in new_colors.values():
                    if len(v.neighbours) == len(verts[0].neighbours):
                        v2 = verts[0]

                        s1 = tuple(sorted([new_coloring[v.graph][n] for n in v.neighbours]))
                        s2 = tuple(sorted([new_coloring[v2.graph][n] for n in v2.neighbours]))

                        if s1 == s2:
                            verts.append(v)
                            added = True
                            break
                
                if not added:
                    new_colors[len(new_colors.keys())] = [v]

                if len(new_colors.keys()) > 1:
                    refined = True

            for verts in new_colors.values():
                color_changes[len(color_changes.keys())] = verts

        for color, verts in color_changes.items():
            for v in verts:
                new_coloring[v.graph][v] = color

    
    return new_coloring


def partition(coloring):
    partitions = {}
    for graph in coloring.keys():
        vert_colors = sorted(coloring[graph].values())
        partitions.setdefault(tuple(vert_colors), []).append(graph)
    
    return [(gr, len(set(col)) == len(col)) for col, gr in partitions.items()]


def count_isomorphism(D, I, G, H, coloring):
    coloring = colorref([G, H], coloring)

    g_colors = sorted([coloring[G][v] for v in G.vertices])
    h_colors = sorted([coloring[H][v] for v in H.vertices])
    
    if g_colors != h_colors:
        return False
    if len(g_colors) == len(set(g_colors)):
        return True

    for i in range(1, len(g_colors)):
        if g_colors[i] == g_colors[i - 1]:
            C = g_colors[i]
            break

    next_color = max(max(coloring[G].values()), max(coloring[H].values())) + 1
    
    for vert in G:
        if coloring[G][vert] == C and vert not in D:
            vert_g = vert
            break

    for vert in H:
        if coloring[H][vert] == C and vert not in I:
            vert_h = vert

            new_coloring = {graph: dict(coloring[graph]) for graph in [G, H]}

            new_coloring[G][vert_g] = next_color
            new_coloring[H][vert_h] = next_color

            if count_isomorphism(D + [vert_g], I + [vert_h], G, H, new_coloring):
                return True


def find_isomorphisms(graphs, coloring):
    isomorphic_pairs = []

    for i in range(len(graphs)):
        for j in range(i + 1, len(graphs)):
            isomorphic = count_isomorphism([], [], graphs[i], graphs[j], coloring)
            if isomorphic: isomorphic_pairs.append((graphs[i], graphs[j]))
    
    return isomorphic_pairs


def count_automorphisms(D, I, G, H, coloring):
    coloring = colorref([G, H], coloring)

    g_colors = sorted([coloring[G][v] for v in G.vertices])
    h_colors = sorted([coloring[H][v] for v in H.vertices])
    
    if g_colors != h_colors:
        return 0
    if len(g_colors) == len(set(g_colors)):
        return 1

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
            num += count_automorphisms(D + [vert_g], I + [vert_h], G, H, new_coloring)
    
    return num


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


def main(path):
    with open(path) as f:
        graphs = load_graph(f, read_list=True)[0]

    init_coloring = {graph: {vert: 0 for vert in graph.vertices} for graph in graphs}

    final_coloring = colorref(graphs, init_coloring)
    for entry in partition(final_coloring):
        if not entry[1]:
            pairs = find_isomorphisms(entry[0], final_coloring)
            for pair in pairs:
                print(f'{graphs.index(pair[0])} {graphs.index(pair[1])}', end=' ')

                G = pair[0]
                G_copy = duplicate_graph(G)
                coloring = {graph: {v: 0 for v in graph.vertices} for graph in [G, G_copy]}

                automorphisms = count_automorphisms([], [], G, G_copy, coloring)
                print(automorphisms)

            

if __name__ == '__main__':
    main('SampleGraphSetBranching/cubes3.grl')
