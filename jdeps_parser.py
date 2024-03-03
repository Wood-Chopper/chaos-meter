import sys

EDGE_SEPARATOR = " -> "


def main():
    args = sys.argv[1:]
    file = open(args[0], "r")
    entries = file.readlines()
    print(parse(entries))


def parse(lines):
    transformed_lines = []  # List to store the transformed lines

    for line in lines:
        # Check if the line is indented, indicating a mapping we're interested in
        if line.startswith("   "):
            splitted = line.split(EDGE_SEPARATOR)
            clean_line = splitted[0] + EDGE_SEPARATOR + splitted[1].split(' ')[0]
            transformed_lines.append(clean_line)

    return transformed_lines


if __name__ == "__main__":
    main()
