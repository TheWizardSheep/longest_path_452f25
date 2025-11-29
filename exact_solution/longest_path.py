from collections import defaultdict
import itertools


# Read in input and build graph adjacency list
def parse_graph():
    graph = defaultdict(list)
    edgeList = []
    numV, numE = [int(num) for num in input().split()]
    for _ in range(numE):
        u, v, w = input().split()
        edgeList.append((u, v))
        graph[u].append((v, int(w)))
    return [graph, edgeList]


# Actual algorithm here
def find_path(graph, edgeList):
    # generate edge combinations
    combinations = []
    for i in range(len(edgeList)):
        combo = list(itertools.combinations(edgeList, i + 1))
        combinations += combo

    # longest path weight, longest path
    biggest = [0, None]
    for combo in combinations:
        continue
        # if legal, get weight & path
        # max(biggest, curr)


    # get all legal paths
    return biggest  # TO BE CHANGED


# Parse the results and format an output
def generate_output(path):
    print("-------------\nOUTPUT:")
    print(len(path))
    for edge in path:
        print(f"{edge} ", end="")
    print("\n")


def main():
    graph, edgeList = parse_graph()
    longest_path = find_path(graph, edgeList)
    generate_output(longest_path)


if __name__ == "__main__":
    main()
