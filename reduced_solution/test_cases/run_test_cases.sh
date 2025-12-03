SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_INTERPRETER="python3"
REDUCTION="../reduction_sol.py"
EXACT_SOL="../../exact_solution/cs412_longestpath_exact.py"

echo Beginning test:

for file in ./*.txt; do
    if [ -f "$file" ]; then
        echo "Testing: $file"
        start=$(date +%s.%N)


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
            echo "HAM FOUND"
        else
            echo "NO HAM FINAL_N=$FINAL_N, expected $EXPECTED"
        fi
        end=$(date +%s.%N)
        elapsed=$(echo "$end - $start" | bc)

    fi
done

wait
echo "All jobs finished." # change this to write to outfile
