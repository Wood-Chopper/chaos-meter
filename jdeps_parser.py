import sys

EDGE_SEPARATOR = " -> "


def main():
    args = sys.argv[1:]
    file = open(args[0], "r")
    entries = file.readlines()
    print(parse(entries))


def parse(lines, exclude_regex=None):
    transformed_lines = []  # List to store the transformed lines

    for line in lines:
        # Check if the line is indented, indicating a mapping we're interested in
        if line.startswith("   "):
            splitted = line.split(EDGE_SEPARATOR)
            from_ = splitted[0].strip()
            to_ = splitted[1].split(' ')[0]
            if not exclude_regex or (not exclude_regex.match(to_) and not exclude_regex.match(from_)):
                clean_line = from_ + EDGE_SEPARATOR + to_
                transformed_lines.append(clean_line)

    return transformed_lines


if __name__ == "__main__":
    main()
