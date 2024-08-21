import argparse
import json
import re
import sys

import networkx as nx

import jdeps_parser
import madge_parser

EDGE_SEPARATOR = " -> "


def main():
	parser = argparse.ArgumentParser(
		prog='Software Entropy calculator',
		description='Tool used to measure various metrics of a software dependency graph.')

	parser.add_argument('-g', '--graph', help='The file containing the dependency graph. Example: "path/to/graph.<jdeps|madge|graph>"', required=True)
	parser.add_argument('-m', '--metric', help='The metric to output', required=True, choices=['cycle', 'in-degree', 'out-degree', 'centrality-degree', 'flow-hierarchy', 'density', 'topology'])
	parser.add_argument('-e', '--exclude',
						help='Regex to identify the components to be excluded from the analysis. This allows to differentiate models from logical components and have more relevant results. Example: ".*\\.model\\..*|.*\\.entity\\..*|.*\\.dto\\..*"',
						required=False)

	if len(sys.argv) == 1:
		parser.print_help(sys.stdout)
		sys.exit(1)
	args = parser.parse_args()

	graph = args.graph
	metric = args.metric
	exclude = args.exclude
	chaos_meter = ChaosMeter(graph, exclude)
	metric_value = chaos_meter.compute_metric(metric)
	print(json.dumps(metric_value, indent=4))


class ChaosMeter:

	def __init__(self, graph, exclude=None):
		self.G = nx.DiGraph()
		self.graph = graph
		self.exclude = exclude
		links = parse(graph, exclude)
		self.ingest(links)

	def ingest(self, entries):
		for entry in entries:
			[source, target] = entry.split(EDGE_SEPARATOR)
			if not self.G.has_node(source):
				self.G.add_node(source)
			if not self.G.has_node(target):
				self.G.add_node(target)
			if self.G.has_node(source) & self.G.has_node(target):
				self.G.add_edge(source, target)

	def compute_metric(self, metric) -> any:
		if metric is None or metric == 'cycle':
			return self.cycle_detector()
		if metric is None or metric == 'in-degree':
			return self.highlight_larger_in_degree()
		if metric is None or metric == 'out-degree':
			return self.highlight_larger_out_degree()
		if metric is None or metric == 'centrality-degree':
			return self.highlight_larger_centrality_degree()
		if metric is None or metric == 'flow-hierarchy':
			return self.flow_hierarchy()
		if metric is None or metric == 'density':
			return self.density()
		if metric is None or metric == 'topology':
			return self.topological_sort()
		return None

	def cycle_detector(self):
		"""Detects cycles in the dependencies"""
		result = sorted(nx.simple_cycles(self.G))
		nbre = len(result)
		report = {
			"total": nbre,
			"cycles": result
		}
		return report

	def highlight_larger_in_degree(self):
		"""Highlight the components with the bigger in-degree"""
		print("In-degree > 3")
		degree = list(self.G.in_degree())
		degree.sort(key=lambda x: x[1], reverse=True)
		degree = [s for s in degree if s[1] > 3]
		return degree

	def highlight_larger_out_degree(self):
		"""Highlight the components with the bigger out-degree"""
		print("Out-degree > 3")
		degree = list(self.G.out_degree())
		degree.sort(key=lambda x: x[1], reverse=True)
		degree = [s for s in degree if s[1] > 3]
		return degree

	def highlight_larger_centrality_degree(self):
		"""Highlight the components with the bigger centrality-degree"""
		print("Centrality-degree > 5")
		in_degree = dict(self.G.in_degree())
		out_degree = dict(self.G.out_degree())
		centrality_degree = {k: in_degree.get(k, 0) + out_degree.get(k, 0) for k in set(in_degree) | set(out_degree)}
		c_list = list(centrality_degree.items())
		c_list.sort(key=lambda x: x[1], reverse=True)
		degree = [s for s in c_list if s[1] > 5]
		return degree

	def flow_hierarchy(self):
		"""Flow hierarchy is defined as the fraction of edges not participating in cycles in a directed graph. The higher, the better"""
		return nx.flow_hierarchy(self.G)

	def density(self):
		"""Density of the graph. The lower, the better"""
		return nx.density(self.G)

	def topological_sort(self):
		"""Topological sorting for Directed Acyclic Graph (DAG) is a linear ordering of vertices such that for every directed edge uv, vertex u comes before v in the ordering."""

		if len(list(nx.simple_cycles(self.G))) > 0:
			print("The graph contains cycles and cannot be topologically sorted")
			return

		# Perform a topological sort to determine a possible order for processing
		topo_sorted_nodes = list(nx.topological_sort(self.G))

		# Initialize layer assignment
		layers = {}
		current_layer = 0

		# Assign layers based on dependencies
		for node in reversed(topo_sorted_nodes):  # Start from the most dependent node
			if self.G.out_degree(node) == 0:  # If the node has no dependencies, assign it the current layer
				layers[node] = current_layer
			else:
				# Find the highest layer among the dependencies
				dep_layers = [layers[dep] for dep in self.G.successors(node)]
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

		return layers



def parse(filename, exclude):
	with open(filename, "r") as file:
		lines = file.readlines()
		extension = filename.split('.')[-1]
		exclude_regex = re.compile(exclude) if exclude else None
		parsed_lines = {
			'madge': lambda v: madge_parser.parse(v, exclude_regex),
			'jdeps': lambda v: jdeps_parser.parse(v, exclude_regex),
			'graph': lambda v: [s.strip() for s in v]
		}[extension](lines)
		return parsed_lines


if __name__ == "__main__":
	main()
