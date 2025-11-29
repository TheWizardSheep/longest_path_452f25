from collections import defaultdict
import itertools

graph = None
edgeList = None


# Read in input and build graph adjacency list
def parse_graph():
    global graph
    global edgeList
    graph = defaultdict(list)
    edgeList = []
    numV, numE = [int(num) for num in input().split()]
    for _ in range(numE):
        u, v, w = input().split()
        edgeList.append((u, v))
        graph[u].append((v, int(w)))


# Return the edge weight
def weight(u, v):
    for node in graph[u]:
        if node[0] == v:
            return node[1]
    raise IndexError("Edge not found")


# Actual algorithm here
def find_path():
    # generate edge combinations
    combinations = []
    for i in range(len(edgeList)):
        combo = list(itertools.permutations(edgeList, i + 1))
        combinations += combo

    # longest path weight, longest path
    biggest = [0, None]
    for combo in combinations:
        # Maintain a set of visited vertices to track cycles
        vertices_seen = set()
        combo_weight = 0
        last_v = None
        still_legal = True
        for u, v in combo:
            vertices_seen.add(u)
            # check for legality (Continuous path and no cycles)
            if ((last_v == None) or (u == last_v) and not (v in vertices_seen)):
                combo_weight += weight(u, v)
            else:
                still_legal = False
                break
            last_v = v

        # Maintain the biggest legal weight
        if still_legal and (combo_weight > biggest[0]):
            biggest[0] = combo_weight
            biggest[1] = combo

    # get all legal paths
    return biggest  # TO BE CHANGED


# Parse the results and format an output
def generate_output(path, weight):
    print("-------------\nOUTPUT:")
    print(weight)
    vertices = []
    for u, v in path:
        if not(u in path):
            vertices.append(u)
        
    for node in vertices:
        print(f"{node} ", end="")
    print(f"{path[-1][1]}")


def main():
    parse_graph()
    weight, path = find_path()
    generate_output(path, weight)


if __name__ == "__main__":
    main()
