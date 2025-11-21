import networkx

def approximation(text):
    # Example LP input:
    # 3 3
    # a b 3
    # b c 4
    # a c 5
    g = networkx.Graph()
    #Handle Input
    lines = text.split("\n")
    v, e = map(int, lines[0].split(" "))
    for i in range(e):
        u, v, w = lines[i+1].split()
        g.add_edge(u, v, weight=int(w))

    #Reduce to max spanning tree
    edgesSorted = sorted(g.edges(data=True), key=lambda x: x[2].get('weight'), reverse=True)
    mst = networkx.Graph()
    for u, v, attr in edgesSorted: #! failure todo
        try: 
            if networkx.has_path(mst, e[0], e[1]):
                continue
            else:
                mst.add_edge(e[0],e[1], e[2].get('weight'))
        except networkx.exception.NodeNotFound as e:
            mst.add_edge(e[0], e[1], e[2].get('weight'))
            continue
    print(mst.edges)
    
    #DFS
    def dfs(curr, curr_path, curr_weight):
        best = (curr_weight, curr_path)
        for neighbor, attr in mst[curr].items():
            if not(curr_path.includes(neighbor)):
                w = attr.get("weight")
                candidate = dfs(neighbor, curr_weight + w, curr_path + [neighbor])
                if candidate[0] > best[0]:
                    best = candidate
        return best
    
    best = (-1000, '')
    for node in mst.nodes:
        weight, path = dfs(node, [], 0)
        best = (weight, path) if weight > best[0] else best

    return best


if __name__ == "__main__":
    text = """3 3\na b 3\nb c 4\na c 5"""
    ans = approximation(text)
    print(ans[1], ans[0])