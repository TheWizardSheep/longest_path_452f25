from collections import defaultdict
import itertools
import argparse

graph = None

parser = argparse.ArgumentParser(description="Find the longest path in a graph")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument(
    "--file", type=str, help="Input file path (if omitted, read from STDIN)"
)

args = parser.parse_args()
input_via_file = args.file
debug = args.debug


# Read in input and build graph adjacency list
def parse_graph():
    global graph
    graph = defaultdict(dict)

    # Read in input as a file instead of STDIN
    if input_via_file is not None:
        with open(input_via_file, "r") as file:
            numV, numE = [int(num) for num in next(file).split()]
            for line in file:
                u, v, w = line.split()
                graph[u][v] = max(graph[u].get(v, -float("inf")), int(w))
                if v not in graph:
                    graph[v] = dict()

    # Read in input as STDIN instead of as a file
    else:
        numV, numE = [int(num) for num in input().split()]
        for _ in range(numE):
            u, v, w = input().split()
            graph[u][v] = max(graph[u].get(v, -float("inf")), int(w))
            if v not in graph:
                graph[v] = dict()


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    for x, y in zip(a, b):
        yield (x, y)


# Actual algorithm here
def find_path():
    # longest path weight, longest path
    biggest = [float('-inf'), None]
    for path_length in range(2, len(graph) + 1):
        for combo in itertools.permutations(graph.keys(), path_length):
            # Maintain a set of visited vertices to track cycles
            # vertices_seen = set()
            combo_weight = 0
            
            # check for legality
            still_legal = True
            this_path = []
            for u, v in pairwise(combo):
                if debug:
                    print(f"testing ({u}, {v})")

                # Check for cycles
                # if v in vertices_seen:
                #     still_legal = False
                #     break

                # Check for legality
                if v in graph[u]:
                    combo_weight += graph[u][v]
                    # vertices_seen.add(u)
                    # vertices_seen.add(v)
                    this_path.append((u, v))

                else:
                    still_legal = False
                    break

            # Maintain the biggest legal weight
            if still_legal and (combo_weight > biggest[0]):
                biggest[0] = combo_weight
                biggest[1] = this_path
    return biggest


# Parse the results and format an output
def generate_output(weight, path):
    if debug:
        print("-------------\nOUTPUT:")

    print(weight)
    if path == None:
        if debug:
            print("No path found!")
        else:
            print()
    else:
        vertices = [path[0][0]]
        for _, v in path:
            vertices.append(v)
        print(" ".join(vertices))


def main():
    parse_graph()
    weight, path = find_path()
    generate_output(weight, path)


if __name__ == "__main__":
    main()
