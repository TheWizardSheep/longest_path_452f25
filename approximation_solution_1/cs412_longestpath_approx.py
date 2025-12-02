from collections import defaultdict
import os
from random import random
import time
import sys

global best_so_far
global deadline

def parse_graph(text):
    """Populate global `graph` and `edgeList` from an input text string.

    `graph` is a dict-of-dicts mapping u->v->weight (directed).
    `edgeList` is a list of (u, v, w) tuples for all edges.
    Returns (numV, numE, start_vertex, end_vertex).
    """
    global graph
    global edgeList
    graph = defaultdict(dict)
    edgeList = []
    lines = text.strip().splitlines()
    if not lines:
        return 0, 0, None, None
    numV, numE = [int(num) for num in lines[0].split()]
    
    start_vertex = None
    end_vertex = None
    
    for i, line in enumerate(lines[1:1+numE]):
        u, v, w = line.split()
        w = int(w)
        # directed graph: store edge only u->v
        graph[u][v] = w
        edgeList.append((u, v, w))
        
        # first vertex is start, second vertex is end
        if i == 0:
            start_vertex = u
            end_vertex = v
    
    return numV, numE, start_vertex, end_vertex

def approximation(text):
    # build graph and edgeList from the provided text
    n, e, start_vertex, end_vertex = parse_graph(text)
    
    if start_vertex is None or end_vertex is None:
        return 0, [], n, e

    # For directed graphs, we don't need MST; just find the longest path from start to end
    # DFS to find heaviest path from start to end in the DAG/directed graph
    def dfs(curr, curr_path, curr_weight):
        if time.time() > deadline:
            return None

        # if we reached the end vertex, return this path
        if curr == end_vertex:
            return (curr_weight, curr_path)

        best = None
        for neighbor, w in graph.get(curr, {}).items():
            if neighbor not in curr_path:
                candidate = dfs(neighbor, curr_path + [neighbor], curr_weight + w)
                if candidate is None:
                    return None  # timeout
                if best is None or candidate[0] > best[0]:
                    best = candidate
                elif candidate[0] == best[0] and best is not None:
                    if random() < 0.5:
                        best = candidate
        
        return best if best is not None else None

    # Start DFS from the start vertex
    result = dfs(start_vertex, [start_vertex], 0)
    
    if result is None:
        return 0, [], n, e
    
    weight, path = result
    return weight, path, n, e


# Modes supported:
# - no stdin and no args: run test_cases/fast_script.txt
# - stdin redirected: read single test from stdin
# - --run-all or -a: run all files in test_cases/ and write aggregated output

time_limit = 10000000
start = time.time()
results = []

base_dir = os.path.dirname(__file__)
test_dir = os.path.join(base_dir, "test_cases")
output_file = os.path.join(base_dir, "output.txt")

# helper to process a single input text and append to results
def process_single(text, label="stdin"):
    print(text)
    weight, path, n, e = approximation(text)
    path_str = " ".join(path) if path else ""
    results.append((label, path_str, weight, n, e, time.time() - start))

# parse simple args so flags can be provided in any order
args = sys.argv[1:]
run_all = False
i = 0
while i < len(args):
    a = args[i]
    if a in ("--run-all", "-a"):
        run_all = True
        i += 1
    elif a in ("-t", "--time-limit"):
        if i + 1 >= len(args):
            print("Missing value for -t/--time-limit")
            sys.exit(1)
        try:
            time_limit = int(args[i + 1])
        except ValueError:
            print("Invalid integer for time limit")
            sys.exit(1)
        i += 2
    else:
        # ignore unknown args (or could error)
        i += 1

# set deadline (global) after parsing args
deadline = time.time() + time_limit

# run-all mode
if run_all:
    if not os.path.isdir(test_dir):
        # raise FileNotFoundError(f"Test directory not found: {test_dir}")
        pass
    for idx, fname in enumerate(sorted(os.listdir(test_dir)), start=1):
        fpath = os.path.join(test_dir, fname)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, "r") as f:
            text = f.read()
        process_single(text, label=fname)

# default: run fast_script.txt inside test_cases
else:
    fast_file = os.path.join(test_dir, "fast_script.txt")
    if not os.path.isfile(fast_file):
        # raise FileNotFoundError(f"fast_script.txt not found in {test_dir}")
        text = """11 13
2 7 3
3 9 19
6 8 6
6 4 -15
8 10 -8
8 11 17
4 10 -20
9 5 11
11 6 -18
3 11 5
2 3 17
9 6 -16
10 2 20
"""
        process_single(text, label="default")
        pass
    else:
        with open(fast_file, "r") as f:
            text = f.read()
        process_single(text, label=os.path.basename(fast_file))

# write results to output.txt
with open(output_file, "w") as out:
    for idx, (label, path_str, weight, n, e, t) in enumerate(results, start=1):
        out.write(f"TEST #{idx}: {label}\n\tV={n}\n\tE={e}\n\tpath={path_str}\n\tweight={weight}\n\tRUNTIME: {t:.4f} seconds\n\n")

if results:
    print(f"Wrote {len(results)} result(s) to {output_file}")
else:
    print("No test cases processed.")
