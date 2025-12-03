– The O running time. Be as specific as possible. For example, if you
are studying a graph problem, express the bounds in terms of V and
E.

Since the algorithm is dominated by various permutations of edges,
the runtime of the algorithm will be almost entirely in terms of E.

Build the graph from input:    O(E).
Permute every edge combination:    O(E!)
    -Check each edge combination for legality:    O(E)
    -Check if the combination is the biggest so far:    O(1)
Traverse the resulting path O(E)

Result:
The permutation and legality check combine for O(E * E!)
The permutation and legality check dominate the algorithm's runtime.
The algorithms runtime is roughly O(E * E!)


– An example of calling the program that works with a sample input file:
python exact_solution/longest_path.py exact_solution/test_cases/test_0.txt
