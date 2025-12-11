Time Complexity:
A single approximation attempt can run in O(V+E). Since the algorithm performs a drunken walk
with no repeated vertices, it can visit at most E edges or V vertices (standard traversal time
complexity). All modifications on a standard DFS are O(1), so no additional overhead is introduced.

Running:
The code below is a demonstration of how to run the program. Graphs are expected to be input through stdin.
`python approx_solution.py [-t <TIME:float>] [-p <THREAD_CT:int>] [-v|--verbose]`

If the program is interrupted by SIGINT, it will promptly terminate and output the best answer seen at that point.
Otherwise, it will terminate after the input time. If no time is input, the program will run infinitely and
the only way to stop execution will be this SIGINT. If no thread count is input, then the program will default to 1.

Running all of the test cases in the testing directory is a simple as running `test_cases/run_test_cases.sh`. The runner
forwards command-line-args to the solver, as well as SIGINTs to allow for anytime behavior for select tests.