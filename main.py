from graph_io import load_graph
from branching import automorphisms, group_isomorphic


def group_gi(graphs, aut=False):
    """
    Prints graphs in groups based on isomorphism, optionally prints automorphisms count for each 
    group.
    Parameters:
        graphs (list): A list of graph objects to analyze.
        aut (bool): Flag to determine whether to count automorphisms.
    """
    groups = group_isomorphic(graphs)
    print(f"{'Sets of isomorphic graphs:':<30}{'# of automorphisms:' if aut else ''}")
    for group in groups:
        aut_count = automorphisms(graphs[group[0]]) if aut else ''
        print(f"{str(group):<30}{aut_count:<30}")


def count_aut(graphs):
    """
    Counts and prints the number of automorphisms for each graph in the list.
    Parameters:
        graphs (list): A list of graph objects.
    """
    print(f"{'Graph Index:':<30}{'# of automorphisms:':<30}")
    for i, graph in enumerate(graphs):
        count = automorphisms(graph)
        print(f"{f'[{i}]':<30}{count:<30}")


def main():
    """
    Main function to read graph files and alyze them based on the file name.
    """
    path = input("Graph file path: ")

    try:
        with open(path, encoding='utf-8') as f:
            graphs = load_graph(f, read_list=True)[0]
    except FileNotFoundError:
        print("File not found.")
        return

    if "GIAut" in path:
        group_gi(graphs, True)
    elif "Aut" in path:
        count_aut(graphs)
    elif "GI" in path:
        group_gi(graphs, False)
    else:
        print("The file couldn't be recognized")


def batch_run(paths):
    """
    Analyzes multiple graph files based on the file name.
    Parameters:
        paths (list): A list of paths to graph files.
    """
    for path in paths:
        print(f'Running: {path}')
        try:
            with open(path, encoding='utf-8') as f:
                graphs = load_graph(f, read_list=True)[0]
        except FileNotFoundError:
            print(f"File not found: {path}")
            continue

        if "GIAut" in path:
            group_gi(graphs, True)
        elif "Aut" in path:
            count_aut(graphs)
        elif "GI" in path:
            group_gi(graphs, False)
        else:
            print(f"The file couldn't be recognized: {path}")
        print('----------------------------------------------------')


if __name__ == '__main__':
    # files = [
    #     # "basic/basic01GI.grl",
    #     "basic/basic02GI.grl",
    #     "basic/basic03GI.grl",
    #     # "basic/basic04GI.grl",
    #     "basic/basic05Aut.grl",
    #     "basic/basic06Aut.grl",
    #     "basic/basic07GIAut.grl"
    # ]
    # batch_run(files)
    main()
