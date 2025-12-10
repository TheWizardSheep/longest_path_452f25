#!/bin/bash

# WARNING 1! This runs 50 tests, with some taking several hours.
# I would reccomend running this with nohup and in the background:
# WARNING 2! If you do run it with nohup and in the background, it may take several calls to killall to end all resulting processes
# nohup ./run_test_cases.sh &

folder="test_cases"
logfile="test_output.log"

# Clear old log file
: > "$logfile"

for file in "$folder"/*; do
{
    start=$(date +%s.%N)

    # Run Python using --file instead of stdin
    output=$(python3 longestpath_exact.py --file "$file" 2>&1)

    end=$(date +%s.%N)
    elapsed=$(echo "$end - $start" | bc)

    {
        echo "==============================="
        echo "File: $file"
        echo "Elapsed: $elapsed seconds"
        echo "Output:"
        echo "$output"
        echo
    } >> "$logfile"

} &
done

wait
echo "All jobs finished. Log written to $logfile"
