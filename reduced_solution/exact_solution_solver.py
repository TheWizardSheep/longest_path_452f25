from collections import defaultdict
import itertools
from itertools import tee

# SLIGHTLY MODIFIED VERSION OF THE EXACT SOLUTION

graph = None
edgeList = None

# Switch to true to see the program actively testing each edge
debug = False


# Read in input and build graph adjacency list
def parse_graph():
    global graph
    global edgeList
    graph = defaultdict(dict)
    edgeList = []
    numV, numE = [int(num) for num in input().split()]
    for _ in range(numE):
        u, v, w = input().split()
        edgeList.append((u, v))
        graph[u][v] = int(w)
        if v not in graph:
            graph[v] = dict()

    # Read in input as a file instead of STDIN
    # with open(sys.argv[1], "r") as file:
    #     numV, numE = [int(num) for num in next(file).split()]
    #     for line in file:
    #         u, v, w = line.split()
    #         edgeList.append((u, v))
    #         graph[u][v] = int(w)
    #     file.close()


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    for x, y in zip(a, b):
        yield (x, y)


# Actual algorithm here
def find_path():
    # longest path weight, longest path
    biggest = [0, None]

    for path_length in range(2, len(graph) + 1):
        # print(graph)
        for combo in itertools.permutations(graph.keys(), path_length):
            # print(path_length,combo)
            # Maintain a set of visited vertices to track cycles
            vertices_seen = set()
            combo_weight = 0
            last_v = None
            still_legal = True
            # check for legality
            this_path = []
            for u, v in pairwise(combo):
                if debug:
                    print(f"testing ({u}, {v})")
                if v in vertices_seen:
                    still_legal = False
                    break
                if v in graph[u]:
                    combo_weight += graph[u][v]
                    vertices_seen.add(u)
                    vertices_seen.add(v)
                    last_v = v
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
