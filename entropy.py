import networkx as nx
import sys
import pprint
import madge_parser
import jdeps_parser

EDGE_SEPARATOR = " -> "

nodeNames = {}
G = nx.DiGraph()
def main():
    args = sys.argv[1:]
    filename = args[0]

    links = parse(filename)
    ingest(links)

    print('--------------------------')
    cycle_detector()
    print('--------------------------')
    highlight_larger_in_degree()
    print('--------------------------')
    density()
    print('--------------------------')


def parse(filename):
    file = open(filename, "r")
    lines = file.readlines()
    extension = filename.split('.')[-1]
    parsed_lines = {
        'madge': lambda v: madge_parser.parse(v),
        'jdeps': lambda v: jdeps_parser.parse(v)
    }[extension](lines)
    return parsed_lines


def ingest(entries):
    for entry in entries:
        [source, target] = entry.split(EDGE_SEPARATOR)
        if (not G.has_node(source)):
            G.add_node(source)
        if (not G.has_node(target)):
            G.add_node(target)
        if (G.has_node(source) & G.has_node(target)):
            G.add_edge(source, target)


# Detects cycles in the dependencies
def cycle_detector():
    result = sorted(nx.simple_cycles(G))
    nbre = len(result)
    if (nbre > 0):
        print(str(nbre) + " cycles detected")
        pprint.pprint(result)
    else:
        print("No cycle detected")

# Highlight the components with the bigger in-degree (first 30)
def highlight_larger_in_degree():
    print("In-degree > 3")
    degree = list(G.in_degree())
    degree.sort(key=lambda x: x[1], reverse=True)
    degree = [s for s in degree if s[1] > 3]
    pprint.pprint(degree)

# Print the density of the graph. The lower, the better
def density():
    print("Density", nx.density(G))


def friendly_name_with_weight(node):
    return nodeNames[node[0]], node[1]


def friendly_name(node_id):
    return nodeNames[node_id]


def friendly_names(node_ids):
    return list(map(friendly_name, node_ids))

if __name__ == "__main__":
    main()
