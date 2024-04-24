from graph import Graph, Vertex


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