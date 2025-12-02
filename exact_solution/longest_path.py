from collections import defaultdict
import itertools
import sys

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
    with open(sys.argv[1], "r") as file:
        numV, numE = [int(num) for num in next(file).split()]
        for line in file:
            u, v, w = line.split()
            edgeList.append((u, v))
            graph[u][v] = int(w)
        file.close()

# Actual algorithm here
def find_path():
    # generate edge combinations
    combinations = itertools.permutations(edgeList, 1)
    for i in range(1, len(edgeList)):
        combo = itertools.permutations(edgeList, i + 1)
        combinations = itertools.chain(combinations, combo)

    # longest path weight, longest path
    biggest = [0, None]
    for combo in combinations:
        # Maintain a set of visited vertices to track cycles
        vertices_seen = set()
        combo_weight = 0
        last_v = None
        still_legal = True
        # check for legality
        for u, v in combo:
            if (debug):
                print(f"testing ({u}, {v})")
            # First edge is always legal
            if (last_v is None):
                combo_weight += graph[u][v]
                vertices_seen.add(u)
                vertices_seen.add(v)
                last_v = v

            # Check for a continous path and for cycles
            elif (u != last_v) or (v in vertices_seen):
                still_legal = False
                break
            
            else:
                combo_weight += graph[u][v]
                vertices_seen.add(v)
                last_v = v

        # Maintain the biggest legal weight
        if still_legal and (combo_weight > biggest[0]):
            biggest[0] = combo_weight
            biggest[1] = combo

    return biggest  


# Parse the results and format an output
def generate_output(weight, path):
    if (debug):
        print("-------------\nOUTPUT:")
    print(weight)
    
    if path == None:
        print("No path found!")
    else:
        vertices = [path[0][0]]
        for _, v in path:
           vertices.append(v)
        
        for node in vertices:
            print(f"{node} ", end="")
        print()


def main():
    parse_graph()
    weight, path = find_path()
    generate_output(weight, path)


if __name__ == "__main__":
    main()
