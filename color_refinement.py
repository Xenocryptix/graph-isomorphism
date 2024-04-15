"""
This program is able to read graphs from a .grl file, with the use of the graph_io module.
Once read, the graph(s) their colors will be refined and an attempt will be made to find
isomorphisms between the graphs.

An usual sequence is:
1. Read graphs from a file
2. Create a disjoint union
3. Refine the colors of this disjoint union
4. Split the union in separate graphs again
5. Check for distinctiveness and isomorphism
"""

from graph import *
from graph_io import *


def color_refinement(graphs: list[Graph]) -> list[Graph]:
    """
    Does color refinement on the graphs provided.
    :param graphs: An array with graphs.
    :return: an array of graphs that has had its colors refined.
    """
    refine_colors(merge_graphs(graphs))
    return graphs


def merge_graphs(graphs: list[Graph]) -> list[Vertex]:
    """
    Creates a disjoint union from all the graphs in the array and already assigns the starting color.
    :param graphs: An array with graphs.
    :return: One single list, which is the disjoint union of all the vertices with basic coloring.
    """
    vertices = list()
    # Merge all vertices into one list
    for graph in graphs:
        for vertex in graph.vertices:
            vertices.append(vertex)
            try:
                vertex.colornum
            except AttributeError:
                vertex.colornum = vertex.degree

    return vertices


def refine_colors(vertices: list[Vertex]):
    """
    Refine the colours of the vertices.
    :param vertices: The vertices to refine.
    """

    change = True
    # Check if the previous iteration yielded the same result (then the colors are stable)
    while change is True:
        change = False

        # Split the vertices based on color
        split_vertices = dict()
        for v in vertices:
            if v.colornum not in split_vertices.keys():
                split_vertices[v.colornum] = set()
            split_vertices.get(v.colornum).add(v)

        # Check for each color if the vertices have the same neighbours and assign new colors based on that
        color_changes = dict()
        for vertices_with_same_color in split_vertices.values():

            # Check to see which vertices with the same color have the same neighbours
            new_colors = dict()
            for vertex in vertices_with_same_color:
                added = False
                for vertices_list in new_colors.values():
                    if have_same_neighbours(vertex, vertices_list[0]):
                        vertices_list.append(vertex)
                        added = True
                        break
                if not added:
                    new_colors[len(new_colors.keys())] = [vertex]
                # A change has been made if the color gets splitted into multiple new colors
                if len(new_colors.keys()) > 1:
                    change = True

            # Add the new colors to the color_changes
            for vertices_list in new_colors.values():
                color_changes[len(color_changes.keys())] = vertices_list

        # Set the coloring according to the values stored in the dictionary
        for color, vertices_list in color_changes.items():
            for vertex in vertices_list:
                vertex.colornum = color


def have_same_neighbours(v1: Vertex, v2: Vertex) -> bool:
    """
    Check if two vertices should have the same color.
    Check if both vertices have already the same color and if their neighbour hoods have the same colours.
    :param v1: The first vertex
    :param v2: The second vertex
    :return: True if both vertices should keep the same color, False otherwise.
    """
    if len(v1.neighbours) == len(v2.neighbours):
        # Sort all the neighbours according to their color, this makes comparing them easier.
        n1 = sorted(list(vertrex.colornum for vertrex in v1.neighbours))
        n2 = sorted(list(vertrex.colornum for vertrex in v2.neighbours))
        return n1 == n2
    return False


def is_distinct(graph: Graph) -> bool:
    """
    Checks if the graph is distinct.
    :requires: The graph should have been color refined.
    :param graph: The graph to check
    :return: True if the graph is distinct
    """
    colors = set(list(v.colornum for v in graph.vertices))
    return len(colors) == len(graph.vertices)


def are_isomorphic(graph1: Graph, graph2: Graph) -> bool:
    """
    Checks if two graphs are indeed isomorphic.
    :param graph1: The first graph
    :param graph2: The second graph
    :return: True if the graphs are isomorphisms of each other, false otherwise.
    """
    if not is_distinct(graph1) or not is_distinct(graph2):
        return False
    color1 = list(v.colornum for v in graph1.vertices)
    color2 = list(v.colornum for v in graph2.vertices)

    return sorted(color1) == sorted(color2)


def do_color_refinement_with_user_input():
    """
    Allows the user to do color refinement on a set of graphs of choice and make a dot file of it
    """
    graph_name = input("Please enter the name of the graph file (leave empty for cref9vert_4_9.grl): ")
    if graph_name == "":
        graph_name = "cref9vert_4_9.grl"

    # Read the graph file.
    try:
        with open('SampleGraphsBasicColorRefinement/' + graph_name) as f:
            graphs = load_graph(f, read_list=True)
    except FileNotFoundError:
        print(f"Unable to open {graph_name}, make sure that it's located in the graphs directory!")
        exit()

    # Ask the user if we should create a .dot file
    create_dot = input("Should the refined graph be exported as .dot? (default: no) ")
    if 'y' in create_dot or 'Y' in create_dot:
        create_dot = True
    else:
        create_dot = False

    # Merges the graphs vertices into a disjoint union, refines the colors and checks if a graph iso-
    # morphism is found. Not all isomorphisms can be found! Only if a graph is distinct we can reliably check for
    # isomorphism .
    graphs = graphs[0]
    color_refinement(graphs)

    graphs_copy = graphs[::]
    for g1 in graphs:
        graphs_copy.remove(g1)
        for g2 in graphs_copy:
            if g1 is not g2 and are_isomorphic(g1, g2):
                print(f"Isomorphism found between:\n{g1}\nAND\n{g2}\n")

    # create a disjunct union of all the graphs
    graph = graphs[0]
    for g in graphs[1:]:
        graph = graph + g

    # TODO: At this moment the isomorphisms are simply printed to the screen. Maybe save them somewhere.

    if create_dot:
        # Write the color refined disjoint union to a .dot file, for visual checks and debugging purposes.
        file_name = 'dot_files/' + graph_name.replace(".grl", "") + "_.dot"
        with open(file_name, 'w') as g:
            write_dot(graph, g)


if __name__ == '__main__':
    do_color_refinement_with_user_input()
