import networkx

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
        best = (curr_weight, curr_path)
        for neighbor, attr in mst[curr].items():
            if neighbor not in curr_path:
                w = attr['weight']
                candidate = dfs(neighbor, curr_path + [neighbor], curr_weight + w)
                if candidate[0] > best[0]:
                    best = candidate
        return best

    best = (-float('inf'), [])
    for node in mst.nodes:
        weight, path = dfs(node, [node], 0)
        if weight > best[0]:
            best = (weight, path)

    return best


if __name__ == "__main__":
    text = """3 3
a b 3
b c 4
a c 5"""
    ans = approximation(text)
    print(ans[1], ans[0])
