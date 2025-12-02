import os
from random import random
import networkx
import time
import sys

global best_so_far
global deadline

def approximation(text):
    g = networkx.Graph()
    
    # Handle Input
    lines = text.strip().split("\n")
    n, e = map(int, lines[0].split())
    for i in range(e):
        u, v, w = lines[i + 1].split()
        g.add_edge(u, v, weight=int(w))

    # Reduce to max spanning tree
    edgesSorted = sorted(g.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    mst = networkx.Graph()
    for u, v, attr in edgesSorted:
        try:
            if not networkx.has_path(mst, u, v):
                mst.add_edge(u, v, weight=attr['weight'])
        except networkx.NodeNotFound:
            mst.add_edge(u, v, weight=attr['weight'])
            continue

    
    # DFS to find heaviest path
    def dfs(curr, curr_path, curr_weight):
        if time.time() > deadline:
            return None

        best_so_far = (curr_weight, curr_path)
        for neighbor, attr in mst[curr].items():
            if neighbor not in curr_path:
                w = attr['weight']
                candidate = dfs(neighbor, curr_path + [neighbor], curr_weight + w)
                if candidate is None:
                    return None
                elif candidate[0] > best_so_far[0]:
                    best_so_far = candidate
                elif candidate[0] == best_so_far[0]:  # break ties randomly
                    if (random() < 0.5):
                        best_so_far = candidate
        return best_so_far
    
    best_so_far = (-float('inf'), [])
    for node in mst.nodes:
        if time.time() > deadline:
            break

        result = dfs(node, [node], 0)

        if result is None:
            break  # timeout inside DFS

        weight, path = result
        if weight > best_so_far[0]:
            best_so_far = (weight, path)

    return best_so_far[0], best_so_far[1], n, e


if __name__ == "__main__":
    # if an alternative path is provided, use that as the test_cases directory
    time_limit = 10000000
    start = time.time()
    results = []
    
    base_dir = os.path.dirname(__file__)
    test_dir = os.path.join(base_dir, "test_cases")
    
    # set deadline before any processing
    deadline = time.time() + time_limit
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "-t":
            time_limit = int(sys.argv[2])
            deadline = time.time() + time_limit
        elif sys.argv[1] == "-d":
            test_dir = os.path.join(base_dir, sys.argv[2])
            if not os.path.isfile(test_dir):
                raise FileNotFoundError(f"Test file not found: {test_dir}")
            with open(test_dir, "r") as f:
                text = f.read()
            weight, path, n, e = approximation(text)
            results.append((1, os.path.basename(test_dir), " ".join(path) if path else "", weight, n, e, time.time() - start))  
    else:
        # default: process test_cases directory
        if not os.path.isdir(test_dir):
            raise FileNotFoundError(f"Test directory not found: {test_dir}")
        for idx, fname in enumerate(sorted(os.listdir(test_dir)), start=1):
            fpath = os.path.join(test_dir, fname)
            if not os.path.isfile(fpath):
                continue
            with open(fpath, "r") as f:
                text = f.read()
            weight, path, n, e = approximation(text)
            path_str = " ".join(path) if path else ""
            results.append((idx, fname, path_str, weight, n, e, time.time() - start))

    output_file = os.path.join(base_dir,"test_cases","output", "output.txt")
    # write all results to output.txt
    with open(output_file, "w") as out:
        for idx, fname, path_str, weight, n, e, t in results:
            out.write(f"TEST #{idx-1}:\n\tV={n}\n\tE={e}\n\tweight={weight}\n\tRUNTIME: {t:.4f} seconds\n\n")

    if results:
        print(f"Wrote {len(results)} results to {output_file}")
    else:
        print("No test files found; no output written.")
