O running time:
    - reduction takes O(m)
    - running the exact solution takes O(E * E!)
    total runtime to find a hamiltonian path is O(m + E * E!)


calling the program:

    To just run the reduction by itself:

        python3 reduced_solution/reduction_sol.py <input_file>

            -- <input_file> is the input containing the undirected weighted graph info

    Running the reduction gives you the name of a new input file to use when
    calling the exact solution solver, to run the exact solver:

        python3 reduced_solution/exact_solution_solver.py <new_input_file>

            -- <new_input_file> would be the filename the reduction returns

    Your output will contain  two lines: the length of the path on one line (as an integer)
    followed by a list of vertices for the path/cycle on the second.

    To know if a hamiltonian cycle exists, compare the first line containing the length of the path
    to the n value in the original <input_file> minus 1. If they are the same it means that every vertex
    was visited and a hamiltonian path exists, else no hamiltonian path exists.
        -- as of right now this only happens automatically in my testing script
