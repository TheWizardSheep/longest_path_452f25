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

def approximation():
    numV, numE = parse_graph()

    # Build Bellman–Ford graph
    mst = build_graph()

    # Collect vertices again
    vertices = set()
    for u, v, _ in edgeList:
        vertices.add(u)
        vertices.add(v)
    vertices = list(vertices)

    best_so_far = (-float("inf"), [])

    def dfs(curr, curr_path, curr_weight):
        nonlocal best_so_far
        if time.time() > deadline:
            return  # Anytime: just bail and keep best_so_far

        if curr_weight > best_so_far[0]:
            best_so_far = (curr_weight, curr_path)

        for neighbor, w in mst.get(curr, {}).items():
            if neighbor not in curr_path:
                dfs(neighbor, curr_path + [neighbor], curr_weight + w)

    # Start DFS from every vertex
    for node in vertices:
        if time.time() > deadline:
            break
        dfs(node, [node], 0)

    return best_so_far[0], best_so_far[1], numV, numE


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
                print(f"Processing TEST #{idx}-{filename}...")
                weight, path, n, e = approximation()
                results.append((idx, os.path.basename(file_path), " ".join(path) if path else "", weight, n, e, time.time() - start))  
                output_file = os.path.join(base_dir,"test_cases","output", "output.txt")
        # write all results to output.txt
        with open(output_file, "w") as out:
            for idx, fname, path_str, weight, n, e, t in results:
                out.write(f"TEST #{idx}-{fname}:\n\tV={n}\n\tE={e}\n\tweight={weight}\n\tpath={path_str}\n\tRUNTIME:{t:.8f} seconds\n\n")

        if results:
            print(f"Wrote {len(results)} results to {output_file}")
        else:
            print("No test files found; no output written.")

    else:
        print("Running from stdin!")
        output_file = os.path.join(base_dir,"test_cases","output", "output.txt")
        with open(output_file, "w") as out:
            weight, path, n, e = approximation()
            out.write(f"V={n}\nE={e}\nweight={weight}\npath={' '.join(path) if path else ''}\n")