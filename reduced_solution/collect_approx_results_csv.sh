#!/bin/zsh




output_csv="approx_results.csv"
echo "test_case,n,bound,actual" > $output_csv

test_dir="../exact_solution/test_cases"



for testfile in $test_dir/*.txt; do
    testname=$(basename "$testfile")
    # Run reduction
    python3 reduction_sol.py "$testfile"
    # Get n (first number in input.txt)
    n=$(head -n 1 input.txt | awk '{print $1}')
    # Run bounds.py and capture output
    bound=$(python3 bounds.py input.txt)
    # Run exact_solution_solver.py and get first line of output (weight)
    actual=$(python3 exact_solution_solver.py < input.txt | head -n 1)
    echo "$testname,$n,$bound,$actual" >> $output_csv
done

echo "Results written to $output_csv"
