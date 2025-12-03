– The O running time. Be as specific as possible. For example, if you
are studying a graph problem, express the bounds in terms of V and
E.

Since the algorithm is dominated by various permutations of edges,
the runtime of the algorithm will be almost entirely in terms of E.

Build the graph from input (graph size dependent on number of edges):    O(E).
Permute every edge combination of every length:    O(E!)
    -Check each edge combination for legality (could be up to E long):    O(E)
    -Check if the combination is the biggest so far:    O(1)
Traverse the resulting path (could be up to E long):    O(E)
Result:
    -The permutation and legality check combine for O(E * E!)
    -The permutation and legality check dominate the runtime.
    -Total runtime: O(2E + E * E!).
    -The algorithm’s runtime simplifies to O(E * E!)



– Examples of calling the program:

- If you would like to input the data via an input file, use --file to provide the file path.
python exact_solution/cs412_longestpath_exact.py --file exact_solution/test_22.txt

- If you would like to input the data via STDIN, call the program and then begin inputting data.
python exact_solution/cs412_longestpath_exact.py
    --> Then input data via STDIN

- To use debug mode, which prints each edge as it is tested, use the --debug flag.
python exact_solution/cs412_longestpath_exact.py --file exact_solution/test_22.txt --debug
