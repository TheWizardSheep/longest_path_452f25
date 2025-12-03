#!/bin/bash

folder="test_cases"
logfile="test_output.log"

# Clear old log file
: > "$logfile"

for file in "$folder"/*; do
{
    start=$(date +%s.%N)
    output=$(python3 longest_path.py "$file" 2>&1)
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


# Candidate for replacement
# #!/bin/bash

# folder="test_cases"
# logfile="test_output.log"

# # Clear old log file
# : > "$logfile"

# for file in "$folder"/*; do
# {
#     start=$(date +%s.%N)

#     # Feed file contents to Python via stdin
#     output=$(python3 longest_path.py < "$file" 2>&1)

#     end=$(date +%s.%N)
#     elapsed=$(echo "$end - $start" | bc)

#     {
#         echo "==============================="
#         echo "File: $file"
#         echo "Elapsed: $elapsed seconds"
#         echo "Output:"
#         echo "$output"
#         echo
#     } >> "$logfile"

# } &
# done

# wait
# echo "All jobs finished. Log written to $logfile"
