import os
import sys
import time
from random import random
from collections import defaultdict

# Globals that you configure at runtime
graph = defaultdict(dict)
edgeList = []
deadline = float("inf")   
file = None               

def parse_graph():
    global graph, edgeList

    graph = defaultdict(dict)
    edgeList = []

    if file is not None:
        with open(file, "r") as f:
            lines = f.read().strip().splitlines()
    else:
        # Read from stdin
        first = sys.stdin.readline().strip()
        if not first:
            return 0, 0
        lines = [first]
        numV, numE = map(int, first.split())
        for _ in range(numE):
            line = sys.stdin.readline().strip()
            if not line:
                continue
            lines.append(line)

    # Parse header again in case we came from file
    numV, numE = map(int, lines[0].split())

    for line in lines[1:]:
        if not line:
            continue
        u, v, w = line.split()
        w = int(w)
        edgeList.append((u, v, w))
        graph[u][v] = w

    return numV, numE


def build_graph():
    # Collect all vertices
    vertices = set()
    for u, v, _ in edgeList:
        vertices.add(u)
        vertices.add(v)
    vertices = list(vertices)

    if not vertices:
        return defaultdict(dict)

    # === UNION-FIND STRUCTURES ===
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    mst = defaultdict(dict)

    num_components = len(vertices)

    # === Boruvka ===
    while num_components > 1:
        best_outgoing = {}

        for u, v, w in edgeList:
            cu, cv = find(u), find(v)
            if cu != cv:
                if cu not in best_outgoing or w > best_outgoing[cu][2]:
                    best_outgoing[cu] = (u, v, w)

        if not best_outgoing:
            break  # cannot connect further; graph is disconnected

        for cu, (u, v, w) in best_outgoing.items():
            if find(u) != find(v):
                mst[u][v] = w
                union(u, v)
                num_components -= 1

    # === Bellman–Ford relaxations ===

    dist = {v: 0 for v in vertices}
    V = len(vertices)

    for _ in range(V - 1):
        improved = False
        for u in mst:
            for v, w in mst[u].items():
                if dist[u] + w > dist[v]:
                    dist[v] = dist[u] + w
                    improved = True
        if not improved:
            break

    return mst

def build_max_acyclic_subgraph():
    """
    Build a Maximum Acyclic Subgraph (MAS) by taking edges in 
    descending weight order and adding them if they do NOT create a cycle.

    Returns:
        dag : adjacency dict {u: {v: weight}}
    """

    # Sort edges by descending weight
    sorted_edges = sorted(edgeList, key=lambda x: x[2], reverse=True)

    dag = defaultdict(dict)

    # Track visited for cycle detection
    # Cycle detection in directed graph via DFS
    def creates_cycle(src, dst):
        """Return True if adding src -> dst creates a cycle."""
        stack = [dst]
        visited = set()

        while stack:
            node = stack.pop()
            if node == src:
                return True
            if node in visited:
                continue
            visited.add(node)
            for nxt in dag.get(node, {}):
                stack.append(nxt)

        return False

    # Build the DAG
    for u, v, w in sorted_edges:
        if u == v:
            continue  # ignore self-loops
        # If adding u->v does NOT create a cycle, keep it
        if not creates_cycle(u, v):
            dag[u][v] = w

    return dag

def approximation():
    numV, numE = parse_graph()

    # Build Bellman–Ford graph
    mst = build_max_acyclic_subgraph()

    # Collect vertices again
    vertices = set()
    for u, v, _ in edgeList:
        vertices.add(u)
        vertices.add(v)
    vertices = list(vertices)

    best_so_far = (-float("inf"), [])

    def beam(mst, vertices, deadline, beam_width=15):

        best_weight = -float("inf")
        best_path = []

        for start in vertices:
            if time.time() > deadline:
                break

            # Each element in the beam is: (weight, path_list)
            beam = [(0, [start])]

            while beam:
                if time.time() > deadline:
                    break

                new_beam = []

                for weight, path in beam:
                    u = path[-1]

                    # Expand neighbors
                    for v, w in mst.get(u, {}).items():
                        if v not in path:  # avoid cycles
                            new_w = weight + w
                            new_path = path + [v]
                            new_beam.append((new_w, new_path))

                            # Track global best
                            if new_w > best_weight:
                                best_weight = new_w
                                best_path = new_path

                # Keep only best beam_width paths
                new_beam.sort(reverse=True, key=lambda x: x[0])
                beam = new_beam[:beam_width]

        return best_weight, best_path

    # Start beam search from every vertex
    weight, path = beam(mst, vertices, deadline)

    return weight, path, numV, numE


if __name__ == "__main__":
    # if an alternative path is provided, use that as the test_cases directory
    start = time.time()
    results = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(base_dir, "test_cases")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "-t":
            time_limit = int(sys.argv[2])
            deadline = time.time() + time_limit
        elif sys.argv[1] == "-d":
            test_dir = os.path.join(base_dir, sys.argv[2])
            if not os.path.isdir(test_dir):
                raise FileNotFoundError(f"Test folder not found: {test_dir}")
            for idx, filename in enumerate(os.listdir(test_dir)):
                file_path = os.path.join(test_dir, filename)
                if (not os.path.isfile(file_path)) or (not filename.endswith(".txt")):
                    continue
                file = file_path
                start = time.time()
                weight, path, n, e = approximation()
                results.append((idx, os.path.basename(file_path), " ".join(path) if path else "", weight, n, e, time.time() - start))  
                output_file = os.path.join(base_dir,"test_cases","output", "output.txt")
        # write all results to output.txt
        for idx, fname, path_str, weight, n, e, t in results:
            print(f"{weight}\n{' '.join(path) if path else ''}")
    else:
        weight, path, n, e = approximation()
        print(f"{weight}\n{' '.join(path) if path else ''}")