from collections import defaultdict

import sys
file = sys.argv[1]

with open(file) as f:
    n, m = map(int, f.readline().split())

    #  input graph
    adj = defaultdict(set)
    for _ in range(m):
        u, v, w = f.readline().split()
        adj[u].add(v)
        adj[v].add


def reduce_LPP(adj, k):
    W = dict()
    for u in adj.keys():
        W[u] = {}
        for v in adj.keys():
            if u == v:
                W[u][v] = 0
            elif v in adj[u]:
                W[u][v] = 0
            else:
                W[u][v] = 1
    K = len(adj.keys()) - k
    return W, K
