#!/bin/zsh




output_csv="approx_results.csv"
echo "test_case,n,bound,actual1,actual2,exact" > $output_csv

test_dir="test_cases"



for testfile in $test_dir/*.txt; do
    testname=$(basename "$testfile")
    # Run reduction
    python3 reduction_sol.py "$testfile"
    # Get n (first number in input.txt)
    n=$(head -n 1 input.txt | awk '{print $1}')
    # Only process if n <= 9
    if [[ $n -le 9 ]]; then
        # Run bounds.py and capture output
        bound=$(python3 bounds.py input.txt)
        # Run approximation.py with time limit and get V value and runtime
    python3 ../approximation_solution_1/approximation.py < input.txt
    actual1=$(grep '^V=' ../approximation_solution_1/test_cases/output/output.txt | awk -F= '{print $2}' | head -n 1)
    actual2=$(python3 ../approx_solution_2/approx_solution.py -t 2 < input.txt | grep '^Longest path found:' | awk '{print $4}' | head -n 1)
    exact=$(python3 exact_solution_solver.py < input.txt | head -n 1)
    echo "$testname,$n,$bound,$actual1,$actual2,$exact" >> $output_csv
    fi
done

echo "Results written to $output_csv"
