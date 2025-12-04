import sys
file = sys.argv[1]


def reduce_input():
    with open(file) as f, open("../input.txt", "w") as i:
        n, m = map(int, f.readline().split())

        # 2m to account for the bidirectional edges we are adding
        i.write(f"{n} {2*m}\n")

        #  give each edge in the unweighted graph an edge weight of 1
        for _ in range(m):
            u, v, _ = f.readline().split()
            i.write(f"{u} {v} 1\n")
            i.write(f"{v} {u} 1\n")

    return "input.txt"


if __name__ == "__main__":
    print(reduce_input())
