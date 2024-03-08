import networkx as nx
import sys
import pprint
import madge_parser
import jdeps_parser
import argparse
import re

EDGE_SEPARATOR = " -> "

nodeNames = {}
G = nx.DiGraph()


def main():

    parser = argparse.ArgumentParser(
        prog='Software Entropy calculator',
        description='Tool used to measure various metrics of a software dependency graph.')

    parser.add_argument('-g', '--graph', help='The file containing the dependency graph. Example: "path/to/graph.<jdeps|madge|graph>"', required=True)
    parser.add_argument('-m', '--model',
                        help='Regex to identify the model components. This allows to differentiate models from logical components and have more relevant results. Example: ".*\\.model\\..*|.*\\.entity\\..*|.*\\.dto\\..*"',
                        required=False)

    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        sys.exit(1)
    args = parser.parse_args()

    links = parse(args.graph, args.model)
    ingest(links)

    print('--------------------------')
    cycle_detector()
    print('--------------------------')
    highlight_larger_in_degree()
    print('--------------------------')
    highlight_larger_out_degree()
    print('--------------------------')
    highlight_larger_centrality_degree()
    print('--------------------------')
    connected_components()
    print('--------------------------')
    betweenness_centrality()
    print('--------------------------')
    closeness_centrality()
    print('--------------------------')
    flow_hierarchy()
    print('--------------------------')
    density()
    print('--------------------------')
    topological_sort()
    print('--------------------------')


def parse(filename, model):
    with open(filename, "r") as file:
        lines = file.readlines()
        extension = filename.split('.')[-1]
        model_regex = re.compile(model) if model else None
        parsed_lines = {
            'madge': lambda v: madge_parser.parse(v, model_regex),
            'jdeps': lambda v: jdeps_parser.parse(v, model_regex),
            'graph': lambda v: [s.strip() for s in v]
        }[extension](lines)
        return parsed_lines


def ingest(entries):
    for entry in entries:
        [source, target] = entry.split(EDGE_SEPARATOR)
        if not G.has_node(source):
            G.add_node(source)
        if not G.has_node(target):
            G.add_node(target)
        if G.has_node(source) & G.has_node(target):
            G.add_edge(source, target)


def cycle_detector():
    """Detects cycles in the dependencies"""
    result = sorted(nx.simple_cycles(G))
    nbre = len(result)
    if (nbre > 0):
        print(str(nbre) + " cycles detected")
        pprint.pprint(result)
    else:
        print("No cycle detected")


def highlight_larger_in_degree():
    """Highlight the components with the bigger in-degree"""
    print("In-degree > 3")
    degree = list(G.in_degree())
    degree.sort(key=lambda x: x[1], reverse=True)
    degree = [s for s in degree if s[1] > 3]
    pprint.pprint(degree)


def highlight_larger_out_degree():
    """Highlight the components with the bigger out-degree"""
    print("Out-degree > 3")
    degree = list(G.out_degree())
    degree.sort(key=lambda x: x[1], reverse=True)
    degree = [s for s in degree if s[1] > 3]
    pprint.pprint(degree)


def highlight_larger_centrality_degree():
    """Highlight the components with the bigger centrality-degree"""
    print("Centrality-degree > 5")
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    centrality_degree = {k: in_degree.get(k, 0) + out_degree.get(k, 0) for k in set(in_degree) | set(out_degree)}
    c_list = list(centrality_degree.items())
    c_list.sort(key=lambda x: x[1], reverse=True)
    degree = [s for s in c_list if s[1] > 5]
    pprint.pprint(degree)


def connected_components():
    """Highlight the strongly connected components"""
    print("Strongly connected components")
    l = list(nx.strongly_connected_components(G))
    l.sort(key=len, reverse=True)
    pprint.pprint([v for v in l if len(v) > 1])


def betweenness_centrality():
    """Classes that frequently appear on shortest paths between other classes might play a crucial role in the communication or data flow within the application.
    These classes are potential candidates for optimization or refactoring to reduce tight coupling."""
    print("Betweenness centrality")
    l = list(nx.betweenness_centrality(G).items())
    l.sort(key=lambda x: x[1], reverse=True)
    pprint.pprint(l[:5])


def closeness_centrality():
    """Identifies classes that can quickly interact with other classes in the system, potentially highlighting good candidates for central services or utilities."""
    print("Closeness centrality")
    l = list(nx.closeness_centrality(G).items())
    l.sort(key=lambda x: x[1], reverse=True)
    pprint.pprint(l[:5])


def flow_hierarchy():
    """Flow hierarchy is defined as the fraction of edges not participating in cycles in a directed graph. The higher, the better"""
    print("Flow hierarchy")
    pprint.pprint(nx.flow_hierarchy(G))


def density():
    """Density of the graph. The lower, the better"""
    print("Density", nx.density(G))


def topological_sort():
    """Topological sorting for Directed Acyclic Graph (DAG) is a linear ordering of vertices such that for every directed edge uv, vertex u comes before v in the ordering."""

    if len(list(nx.simple_cycles(G))) > 0:
        print("The graph contains cycles and cannot be topologically sorted")
        return

    # Perform a topological sort to determine a possible order for processing
    topo_sorted_nodes = list(nx.topological_sort(G))

    # Initialize layer assignment
    layers = {}
    current_layer = 0

    # Assign layers based on dependencies
    for node in reversed(topo_sorted_nodes):  # Start from the most dependent node
        if G.out_degree(node) == 0:  # If the node has no dependencies, assign it the current layer
            layers[node] = current_layer
        else:
            # Find the highest layer among the dependencies
            dep_layers = [layers[dep] for dep in G.successors(node)]
            layers[node] = max(dep_layers) + 1  # Place the node above its highest dependency

    # Since the process can assign higher numbers to "higher" layers (contrary to intuitive understanding),
    # we may invert the layers to make the "highest" layer have the smallest number
    max_layer = max(layers.values())
    node_layers = {node: max_layer - layer for node, layer in layers.items()}

    # Invert the mapping to have layer IDs as keys and component names as values
    layers = {}
    for node, layer in node_layers.items():
        if layer not in layers:
            layers[layer] = [node]
        else:
            layers[layer].append(node)

    print("Layers (layer ID: [component names]):")
    for layer in sorted(layers):
        pprint.pprint(f"{layer}: {layers[layer]}")


if __name__ == "__main__":
    main()