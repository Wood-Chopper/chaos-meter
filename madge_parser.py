import sys


def main():
	args = sys.argv[1:]
	file = open(args[0], "r")
	entries = file.readlines()
	print(parse(entries))


def parse(lines, exclude_regex=None):
	parent = None  # Variable to keep track of the current parent node
	parent_is_model = False  # Variable to keep track of the current parent node
	relationships = []  # List to store the parent-child relationships

	for line in lines:
		stripped_line = line.strip()  # Remove leading and trailing whitespace
		if line.startswith("  ") and not parent_is_model:  # Check if the line is indented (assuming 2 spaces for indentation)
			# This is a child node, so create a relationship entry
			if not exclude_regex or not exclude_regex.match(stripped_line):
				relationships.append(parent + ' -> ' + stripped_line)
		if line and not line.startswith("  "):
			parent = stripped_line
			parent_is_model = exclude_regex and exclude_regex.match(parent)

	return relationships


if __name__ == "__main__":
	main()
