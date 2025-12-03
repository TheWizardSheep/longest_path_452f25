Time Complexity:
A single approximation attempt can run in O(V+E). Since the algorithm performs a drunken walk
with no repeated vertices, it can visit at most E edges or V vertices (standard traversal time
complexity). All modifications on a standard DFS are O(1), so no additional overhead is introduced.

Running:
The code below is a demonstration of how to run the program. Graphs are expected to be input through stdin.
`python approx_solution.py [-t <TIME:int>] [-p <THREAD_CT:int>] [-v|--verbose]`
If the program is interrupted by SIGINT, it will promptly terminate and output the best answer seen at that point.
Otherwise, it will terminate after the input time.