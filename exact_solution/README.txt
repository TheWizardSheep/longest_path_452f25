– The O running time. Be as specific as possible. For example, if you
are studying a graph problem, express the bounds in terms of V and
E.

Since the algorithm is dominated by various permutations of vertices,
the runtime of the algorithm will be almost entirely in terms of V.

Build the graph from input:    O(E).
Permute every vertex combination of every length:    O(V!)
    -Check each vertex combination for legality (could be up to V long):    O(V)
    -Check if the combination is the biggest so far:    O(1)
Traverse the resulting path (could be up to V long):    O(V)
Result:
    -The permutation and legality check combine for O(V * V!)
    -The permutation and legality check dominate the runtime.
    -The algorithm’s runtime simplifies to O(V * V!)



– Examples of calling the program:
(The examples' command line calls assume you are in the longest_path_452f25 directory, not the exact_solution directory)

- If you would like to input the data via an input file, use --file to provide the file path.
python exact_solution/longestpath_exact.py --file exact_solution/test_result_data/test_case_data_DONOTCHANGE/test_20.txt

- If you would like to input the data via STDIN, call the program and then begin inputting data.
python exact_solution/longestpath_exact.py
    --> Then input data via STDIN

- To use debug mode, which prints each edge as it is tested, use the --debug flag.
python exact_solution/longestpath_exact.py --file exact_solution/test_result_data/test_case_data_DONOTCHANGE/test_20.txt --debug
