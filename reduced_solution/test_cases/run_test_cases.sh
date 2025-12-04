SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_INTERPRETER="python3"
REDUCTION="../reduction_sol.py"
EXACT_SOL="../exact_solution_solver.py"
RESULTS="$SCRIPT_DIR/../results.txt"

echo Beginning test:

for file in ./*.txt; do
    if [ -f "$file" ]; then
        echo "Testing: $file"
        START=$(date +%s.%N)

        # reduce to LPP input
        NEW_INPUT=$($PYTHON_INTERPRETER $REDUCTION "$file")

         # grab the n from the input
        EXPECTED_N=$(head -n1 "../$NEW_INPUT" | awk '{print $1}')

        # run LPP
        EXACT_OUTPUT=$($PYTHON_INTERPRETER "$EXACT_SOL" "$@" < "../$NEW_INPUT")

        # final n
        FINAL_N=$(echo "$EXACT_OUTPUT" | head -n1 )

        # expected n
        EXPECTED=$(($EXPECTED_N - 1))

        # was n - 1 verticies visited
        if [ "$FINAL_N" -eq "$EXPECTED" ]; then
            echo "HAM FOUND" >> "$RESULTS"
        else
            echo "NO HAM FINAL_N=$FINAL_N, expected $EXPECTED" >> "$RESULTS"
        fi

        END=$(date +%s.%N)
        ELAPSED=$(echo "$END - $START" | bc)
        echo Time: $ELAPSED >> "$RESULTS"
    fi
done

wait
echo "All jobs finished." # change this to write to outfile
