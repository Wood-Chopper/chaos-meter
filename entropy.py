import networkx as nx
import sys
import pprint
import itertools

EDGE_SEPARATOR = "<-[#595959,plain]-"

nodeNames = {}
G = nx.DiGraph()
def main():
    args = sys.argv[1:]
    file = open(args[0], "r")
    entries = file.readlines()
    read_puml(entries)

    cycle_detector()
    #highlight_strongly_connected()
    highlight_larger_in_degree()
    highlight_page_rank()
    density()


def read_puml(entries):
    for entry in entries:
        if entry.__contains__("class") & entry.__contains__(" as ") & (not entry.__contains__(".spec.")):
            nodeId = entry.split(" ")[1].strip()
            nodeName = entry.split(" ")[3].strip().replace('\"', '')
            G.add_node(nodeId)
            nodeNames[nodeId] = nodeName
    for entry in entries:
        if entry.__contains__(EDGE_SEPARATOR):
            source = entry.split(EDGE_SEPARATOR)[0].strip()
            target = entry.split(EDGE_SEPARATOR)[1].strip()
            if (G.has_node(source) & G.has_node(target)):
                if (not G.has_edge(source, target)):  # simple edge, no weight
                    G.add_edge(source, target)


# Detects cycles in the dependencies
def cycle_detector():
    result = sorted(nx.simple_cycles(G))
    friendlyfied = list(map(friendly_names, result))
    if friendlyfied != []:
        print("Cycles detected")
        pprint.pprint(friendlyfied)

# Highlight the strongly connected components (first 30)
def highlight_strongly_connected():
    print("Strongly connected components")
    result = itertools.islice(nx.strongly_connected_components(G), 100)
    friendlyfied = list(map(friendly_names, result))
    pprint.pprint(friendlyfied)


# Highlight the components with the bigger in-degree (first 30)
def highlight_larger_in_degree():
    print("In-degree")
    degree = list(G.in_degree())
    degree.sort(key=lambda x: x[1], reverse=True)
    friendlyfied = list(map(friendly_name_with_weight, degree[:30]))
    pprint.pprint(friendlyfied)


# Highlight the components with the bigger page raking (first 30)
def highlight_page_rank():
    print("Page rank")
    result = nx.pagerank(G).items()
    result = sorted(result, key=lambda x: x[1], reverse=True)
    friendlyfied = list(map(friendly_name_with_weight, result[:30]))
    pprint.pprint(friendlyfied)


# Print the density of the graph. The lower, the better
def density():
    print("Density")
    print(nx.density(G))


def friendly_name_with_weight(node):
    return nodeNames[node[0]], node[1]


def friendly_name(node_id):
    return nodeNames[node_id]


def friendly_names(node_ids):
    return list(map(friendly_name, node_ids))

if __name__ == "__main__":
    main()
