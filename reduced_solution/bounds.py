import sys


def read_input(filename):
    edges = []
    with open(filename) as f:
        n, m = map(int, f.readline().split())
        for _ in range(m):
            u, v, w = f.readline().split()
            edges.append(int(w))  # store only the weight
    return n, edges


def find_upper_bound(filename):
    n, weights = read_input(filename)

    # largest edge weight of the total graph * number of edges
    return max(weights) * (n - 1)


if __name__ == "__main__":
    ub = find_upper_bound(sys.argv[1])
    print(ub)
