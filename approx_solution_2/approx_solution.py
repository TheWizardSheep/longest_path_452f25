from collections import defaultdict
import argparse
import time

parser = argparse.ArgumentParser(description="An approximation algorithm for the longest path problem")
parser.add_argument("-t", type=int, help="The maximum running time of the program")
args = parser.parse_args()
t = args.t if not args.t is None else float("inf")
start_time = time.time()

while True:
    cur_time = time.time()
    if (start_time + t <= cur_time):
        break

V, E = map(int, input().split())
adj = defaultdict(list)
for e in range(E):
    u, v, w = input().split()
    adj[u].append((v, int(w)))

print(adj)
