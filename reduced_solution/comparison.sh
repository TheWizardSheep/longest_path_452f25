#!/bin/zsh

# Output CSV file
output_csv="n9_comparison_results.csv"
echo "test_case,upper_bound,wills_solution,nates_solution,bens_exact_solution" > $output_csv

# Directory containing test cases
test_dir="../exact_solution/test_cases"

for testfile in $test_dir/*.txt; do
    testname=$(basename "$testfile" .txt)

    # Run reduction
    python3 reduction_sol.py "$testfile" > /dev/null

    # Get n (first number in input.txt)
    n=$(head -n 1 input.txt | awk '{print $1}')

    # Skip if n != 7
    if [ "$n" -ne 12 ]; then
        continue
    fi

    echo "Processing: $testname (n=$n)"

    # Run bounds.py and capture output
    upper_bound=$(python3 bounds.py input.txt)

    echo "Running exact solution: $testname (n=$n)"

    # Run exact_solution_solver.py and get first line (longest path weight)
    bens_exact=$(python3 exact_solution_solver.py < input.txt | head -n 1)

    echo "Running approximation 1: $testname (n=$n)"

    # Run approximation.py and extract weight from output file
    python3 ../approximation_solution_1/approximation.py < input.txt > /dev/null
    wills_solution=$(grep '^weight=' ../approximation_solution_1/test_cases/output/output.txt | awk -F= '{print $2}' | head -n 1)

    echo "Running approximation 2: $testname (n=$n)"

    # Run approx_solution.py and extract weight from output
    nates_solution=$(python3 ../approx_solution_2/approx_solution.py -t 5 < input.txt | grep '^Longest path found:' | awk '{print $4}')

    # Write to CSV
    echo "$testname,$upper_bound,$wills_solution,$nates_solution,$bens_exact" >> $output_csv
done
trap - SIGINT

echo "Results written to $output_csv"
