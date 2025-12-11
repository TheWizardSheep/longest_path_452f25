import os
import random

"""
Run this file to generate different graphs as test cases for the solver.
They will be written to files in the local test_cases directory.
The generator will not clear the directory before writing to it, but it will overwrite files 
that existed before generating new tests. All of the constants below can be modified to modify the 
functionality of the generator.

Randomization process overview:
    - generate a random V in range
    - generate a random E in range
    - E will be capped at the maximum number of edges in a V-vertex graph
    - generate E random edges with random weights (either with or without duplicates based on the constants)
"""


# Constants
NUM_CASES = 30
MIN_EDGES = 5000 # forced to be at least 1
MAX_EDGES = 20000
MIN_VERTICES = 500 # forced to be at least 2
MAX_VERTICES = 750
MAX_WEIGHT = 1000
ALLOW_DUPLICATE_EDGES = False  # can two edges u->v with different weights exist?
ALLOW_NEGATIVE_WEIGHTS = True # weights will either range from [0, MAX_WEIGHT] or [-MAX_WEIGHT, MAX_WEIGHT]
UNDIRECTED = False  # adds identical reversed edges to each edge generaated
SEED = None  # not really needed, can be used for deterministic randomness if that's useful in the future

# find the test_cases directory for file outputs
TEST_DIR = os.path.join(os.path.dirname(__file__), "test_cases")
os.makedirs(TEST_DIR, exist_ok=True)

# seed the randomness if a seed is provided
if SEED is not None:
    random.seed(SEED)


def generate_graph():
    # randomly pick V and E from a valid range
    V = random.randint(max(2, MIN_VERTICES), MAX_VERTICES)
    max_possible_edges = V * (V - 1)
    max_edges = min(MAX_EDGES, max_possible_edges)
    E = random.randint(max(1, min(MIN_EDGES, max_edges)), max_edges)

    # generate a collection of edges
    edges = set() if ALLOW_DUPLICATE_EDGES else dict()
    while len(edges) < E:
        u = str(random.randint(1, V))
        v = str(random.randint(1, V))
        if u != v:
            w = random.randint(-MAX_WEIGHT if ALLOW_NEGATIVE_WEIGHTS else 0, MAX_WEIGHT)
            if ALLOW_DUPLICATE_EDGES:
                edges.add((u, v, w))
                if UNDIRECTED:
                    edges.add((v, u, w))
            else:
                edges[(u, v)] = w
                if UNDIRECTED:
                    edges[(v, u)] = w

    # flatten the dict to a set if saving duplicate edges
    if not ALLOW_DUPLICATE_EDGES:
        edges = {(u, v, w) for (u, v), w in edges.items()}

    return V, len(edges), list(edges)


def write_test_case(idx, V, E, edges):
    # write to a file in the specified input format
    filename = os.path.join(TEST_DIR, f"test_{idx}.txt")
    with open(filename, "w") as f:
        f.write(f"{V} {E}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")
    print(f"Generated {filename}")


def main():
    # run the generator the specified number of times
    for i in range(NUM_CASES):
        V, E, edges = generate_graph()
        write_test_case(i, V, E, edges)


if __name__ == "__main__":
    main()
