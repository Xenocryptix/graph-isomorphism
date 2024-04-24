from graph_io import load_graph
from graph import Graph, Vertex, Edge
from colorref import colorref, partition
from branching import find_isomorphisms, automorphisms


def GI(graphs, aut=False):
    init_coloring = {graph: {vert: 0 for vert in graph.vertices}
                     for graph in graphs}
    
    coloring = colorref(graphs, init_coloring)
    partitions = partition(coloring)

    for entry in partitions:
        if not entry[1] and len(entry[0]) > 1:
            pairs = find_isomorphisms(entry[0], coloring)
            for pair in pairs:
                print(
                    f'[{graphs.index(pair[0])} {graphs.index(pair[1])}]', end=' ')

                if aut:
                    count = automorphisms(pair[0], coloring)
                    print(count)
                else:
                    print()
        else:
            for graph in entry[0]:
                print(f'[{graphs.index(graph)}]', end=' ')
                if aut:
                    count = automorphisms(graph, coloring)
                    print(count)
                else:
                    print()


def main():
    path = input("Graph file path: ")

    try:
        with open(path) as f:
            graphs = load_graph(f, read_list=True)[0]
    except FileNotFoundError:
        print("File not found.")
        return

    if "GIAut" in path or "Aut" in path:
        GI(graphs, True)
    elif "GI" in path:
        GI(graphs, False)
    else:
        print("The file couldn't be recognized")


if __name__ == '__main__':
    main()
