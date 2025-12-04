#!/bin/zsh

# Output CSV file
output_csv="bounds_n_results.csv"
echo "test,n,bound" > $output_csv


# Directory containing test cases
test_dir="../exact_solution/test_cases"

for testfile in $test_dir/*.txt; do
    testname=$(basename "$testfile")
    # Run reduction
    python3 reduction_sol.py "$testfile"
    # Get n (first number in input.txt)
    n=$(head -n 1 input.txt | awk '{print $1}')
    # Run bounds.py and capture output
    bound=$(python3 bounds.py)
    # Write to CSV
    echo "$testname,$n,$bound" >> $output_csv
done

echo "Results written to $output_csv"
