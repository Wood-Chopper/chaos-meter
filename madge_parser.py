import sys

def main():
    args = sys.argv[1:]
    file = open(args[0], "r")
    entries = file.readlines()
    print(parse(entries))

def parse(lines):
    parent = None  # Variable to keep track of the current parent node
    relationships = []  # List to store the parent-child relationships

    for line in lines:
        stripped_line = line.strip()  # Remove leading and trailing whitespace
        if line.startswith("  "):  # Check if the line is indented (assuming 2 spaces for indentation)
            # This is a child node, so create a relationship entry
            if parent is not None:  # Ensure there is a valid parent
                relationships.append(f"{parent} -> {stripped_line}")
        if line and not line.startswith("  "):
            parent = stripped_line

    return relationships

if __name__ == "__main__":
    main()
