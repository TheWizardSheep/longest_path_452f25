from collections import defaultdict
from multiprocessing import Process, Manager
import argparse
import time
import random

""" 
One-Shot approximation:

Arguments:
    v: a vertex on the graph from which to start searching

Logic:
* walk out, choosing a next edge using outgoing edge weights as random weights until the walk cannot continue
* might as well keep going until no path can be found, if we track cur_longest at each step then it is fine to do so
"""


def run_approximation(v, adj):
    longest = pathlen = 0
    path = [v]
    best_path = []
    visited = set(path)
    while True:
        # find the frontier and assign arbitrary odds based on their weight
        frontier = []
        odds = []
        for dv, dw in adj[v]:
            if not dv in visited:
                frontier.append((dv, dw))
                odds.append(dw)

        # stop when can't continue
        if len(frontier) == 0:
            break
        
        # shift weights to be strictly above 0
        # negatives and zeros become 1
        odds = [max(w,1) for w in odds]

        
        # pick a vertex to go to next, and update the path accordingly
        dv, dw = random.choices(frontier, weights=odds)[0]
        pathlen += dw
        path.append(dv)
        visited.add(dv)
        v = dv
        # update best
        if pathlen > longest:
            longest = pathlen
            best_path = path.copy()
        

    return longest, "->".join(best_path)


def worker(start_time, t, adj, best_result, verbose=False):
    try:
        import random, time
        while True:
            cur_time = time.time()
            if start_time + t <= cur_time:
                break
            v = random.choice(list(adj.keys()))
            dlen, dpath = run_approximation(v, adj)
            if verbose and dlen > 0:
                print(f"{dlen} : {dpath}")
            # update shared best result safely
            if dlen > best_result["len"]:
                best_result["len"] = dlen
                best_result["path"] = dpath
                if verbose:
                    print("New Best!")
    except KeyboardInterrupt:
        print("Stopping thread...")


if __name__ == "__main__":

    # read in command line args
    parser = argparse.ArgumentParser(
        description="An approximation algorithm for the longest path problem"
    )
    parser.add_argument("-t", type=int, help="The maximum running time of the program")
    parser.add_argument(
        "-p",
        type=int,
        help="The number of parallel processes for the program to run in",
    )
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('-v', action='store_true', help='Enable verbose output.')
    args = parser.parse_args()
    t = args.t if not args.t is None else float("inf")
    num_processes = args.p if not args.p is None else 1
    verbose = args.v or args.verbose
    start_time = time.time()

    # input a graph
    V, E = map(int, input().split())
    adj = defaultdict(list)
    for e in range(E):
        u, v, w = input().split()
        adj[u].append((v, int(w)))


    # run for time t
    with Manager() as manager:
        best_result = manager.dict({"len": 0, "path": ""})
        try:
            processes = []
            for _ in range(num_processes):
                p = Process(
                    target=worker, args=(start_time, t, adj, best_result, verbose)
                )
                processes.append(p)
                p.start()
            for p in processes:
                p.join()
            print("Time limit reached!")
        except KeyboardInterrupt:
            print("Keyboard Interrupted!")
            for p in processes:
                p.terminate()
            for p in processes:
                p.join()

        print(f"Longest path found: {best_result['len']}")
        print(f"Path: {best_result['path']}")
