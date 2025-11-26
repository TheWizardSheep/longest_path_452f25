from collections import defaultdict
import argparse
import time

# read in command line args
parser = argparse.ArgumentParser(
    description="An approximation algorithm for the longest path problem"
)
parser.add_argument("-t", type=int, help="The maximum running time of the program")
args = parser.parse_args()
t = args.t if not args.t is None else float("inf")
start_time = time.time()

# run for time t
while True:
    cur_time = time.time()
    if start_time + t <= cur_time:
        break

# input a graph
V, E = map(int, input().split())
adj = defaultdict(list)
for e in range(E):
    u, v, w = input().split()
    adj[u].append((v, int(w)))

print(adj)

""" 
One-Shot approximation:

* choose a random starting vertex (maybe random weighting based on outgoing edge weights?)
* dfs out, choosing an edge (random weighting based on edge weights)
* might as well keep going until no path can be found, if we track curbest at each step then it is fine to do so

"""

