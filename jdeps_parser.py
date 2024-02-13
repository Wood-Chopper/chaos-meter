import sys

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
            # Extract the mapping part before the jar file reference
            mapping_part = ' '.join(line.strip().split()[:-1])
            transformed_lines.append(mapping_part)

    return transformed_lines

if __name__ == "__main__":
    main()
