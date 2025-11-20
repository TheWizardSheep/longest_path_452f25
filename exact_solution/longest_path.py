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
    #generate edge combinations
    combinations = []
    for i in range(len(edgeList)):
        combinations.append(list(itertools.combinations(edgeList, i+1)))
    print(list(combinations))
    return 0 #TO BE CHANGED

# Parse the results and format an output
def generate_output():
    return "" #TO BE CHANGED


def main():
    graph, edgeList = parse_graph()
    find_path(graph, edgeList)
    


if __name__ == "__main__":
    main()