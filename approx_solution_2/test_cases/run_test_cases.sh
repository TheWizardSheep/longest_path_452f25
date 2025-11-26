PYTHON_INTERPRETER="python"
PYTHON_SCRIPT="../approx_solution.py"

for file in *; do
    extension="${file##*.}"
    if [ -f "$file" ] && [ "$extension" = "txt" ]; then
        echo "Testing: $file"
        $PYTHON_INTERPRETER "$PYTHON_SCRIPT" "$@" < "$file"
    fi
done
