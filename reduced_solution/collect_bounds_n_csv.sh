#!/bin/zsh


# Output CSV file
output_csv="bounds_n_results.csv"
echo "test,n,bound,actual" > $output_csv


# Directory containing test cases
test_dir="test_cases"


for testfile in $test_dir/*.txt; do
    testname=$(basename "$testfile")
    # Run reduction
    python3 reduction_sol.py "$testfile"
    # Get n (first number in input.txt)
    n=$(head -n 1 input.txt | awk '{print $1}')
    # Run bounds.py and capture output
    bound=$(python3 bounds.py input.txt)
    # Run exact_solution_solver.py and get first line of output
    actual=$(python3 exact_solution_solver.py < input.txt | head -n 1)
    # Write to CSV
    echo "$testname,$n,$bound,$actual" >> $output_csv
done

echo "Results written to $output_csv"
