def colorref(graphs, coloring):
    """
    Refines a starting coloring of a list of graphs based on their neighborhoods.
    Parameters:
        graphs (list): A list of graphs.
        coloring (dict): Initial coloring of the graphs.
    Returns:
        dict: A dictionary of refined colorings for all graphs.
    """
    vertices = [vert for graph in graphs for vert in graph.vertices]

    # Deep copy of coloring
    new_coloring = {graph: dict(coloring[graph]) for graph in graphs}

    refined = True
    while refined:
        refined = False

        # Group vertices by color (color -> [vertices])
        color_classes = {}
        for v in vertices:
            color = new_coloring[v.graph][v]
            color_classes.setdefault(color, []).append(v)

        next_color = 0

        # Compare neighbors of vertices with the same color
        for color, same_col_verts in color_classes.items():
            new_classes = {}
            for v in same_col_verts:
                # Track if the neighbourhood coloring already known in new_classes
                known_signature = False

                # Compare the neighbourho with a representative vertex of each class
                for verts in new_classes.values():
                    if len(v.neighbours) == len(verts[0].neighbours):
                        v2 = verts[0]

                        # Compute the neighbour signature of both vertices
                        s1 = tuple(sorted([new_coloring[v.graph][n]
                                   for n in v.neighbours]))
                        s2 = tuple(sorted([new_coloring[v2.graph][n]
                                   for n in v2.neighbours]))

                        # If neighbourhoods are the same, they get the same new color
                        if s1 == s2:
                            verts.append(v)
                            known_signature = True
                            break

                # New neighbourhood signature (in this iteration), new color
                if not known_signature:
                    new_classes[next_color] = [v]
                    next_color += 1

                # Refined if this color class is split into multiple classes
                if len(new_classes.keys()) > 1:
                    refined = True

            # Update the coloring
            for col, verts in new_classes.items():
                for v in verts:
                    new_coloring[v.graph][v] = col

    return new_coloring
