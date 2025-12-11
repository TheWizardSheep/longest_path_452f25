– The O running time. Be as specific as possible. For example, if you
are studying a graph problem, express the bounds in terms of V and
E.

Since the algorithm is dominated by variable length permutations of vertices,
the runtime of the algorithm will be almost entirely in terms of V.

Build the graph from input:    O(V + E).
For every possible path length:    O(V)
    -For every vertex permutation of that length:    O(V!)
        -Zip consecutive vertices into edges:    O(V)
        -Check each path for legality:    O(V)
    -Update the longest path if necessary:    O(1)
Traverse and output the longest path (could be up to V long):    O(V)
Total runtime:    O(V^2 * V!)


– Examples of calling the program:
(The examples' command line calls assume you are in the longest_path_452f25 directory, not the exact_solution directory)

- If you would like to input the data via an input file, use --file to provide the file path.
python exact_solution/longestpath_exact.py --file exact_solution/test_result_data/test_case_data_DONOTCHANGE/test_20.txt

- If you would like to input the data via STDIN, call the program and then begin inputting data.
python exact_solution/longestpath_exact.py
    --> Then input data via STDIN

- To use debug mode, which prints each edge as it is tested, use the --debug flag.
python exact_solution/longestpath_exact.py --file exact_solution/test_result_data/test_case_data_DONOTCHANGE/test_20.txt --debug
