#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_INTERPRETER="python"
PYTHON_SCRIPT="$SCRIPT_DIR/../approx_solution.py"

logfile=$SCRIPT_DIR/test_output.log

# Clear old log file
: > "$logfile"

trap '' SIGINT
for file in $SCRIPT_DIR/*.txt; do
{
    echo Testing ${file##*/}
    start=$(date +%s.%N)
    output=$($PYTHON_INTERPRETER $PYTHON_SCRIPT $@ < $file 2>&1)
    end=$(date +%s.%N)

    elapsed=$(awk "BEGIN {print $end - $start}")

    {
        echo =============================================
        echo File: ${file##*/}
        echo Elapsed: $elapsed seconds
        echo Output:
        echo $output
        echo
    } >> $logfile

}
done
trap - SIGINT

wait
echo "All jobs finished. Log written to $logfile"