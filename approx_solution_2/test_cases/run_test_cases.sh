SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_INTERPRETER="python"
PYTHON_SCRIPT="$SCRIPT_DIR/../approx_solution.py"

echo Beginning test:

trap '' SIGINT   # ignore Ctrl-C in the shell
for file in "$SCRIPT_DIR"/*.txt; do
    if [ -f "$file" ]; then
        echo "Testing: $file"
        # Run Python, but don't let Ctrl-C kill the whole loop
        $PYTHON_INTERPRETER "$PYTHON_SCRIPT" "$@" < "$file"
    fi
done
trap - SIGINT    # restore normal Ctrl-C handling
