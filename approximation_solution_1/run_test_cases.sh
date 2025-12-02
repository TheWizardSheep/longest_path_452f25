#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# The python file name
PY_FILE="${SCRIPT_DIR}/approximation.py"

# If no arguments, run from stdin
if [ $# -eq 0 ]; then
    echo "Running in stdin mode..."
    python3 "$PY_FILE"
    exit 0
fi

# Otherwise forward command line arguments to the python program
case "$1" in
    -t)
        if [ $# -ne 2 ]; then
            echo "Usage: ./run_test_cases.sh -t <seconds>"
            exit 1
        fi
        python3 "$PY_FILE" -t "$2"
        ;;

    -d)
        if [ $# -ne 2 ]; then
            echo "Usage: ./run_test_cases.sh -d <test_folder>"
            exit 1
        fi
        python3 "$PY_FILE" -d "$2"
        ;;

    *)
        echo "Unknown option: $1"
        echo "Usage:"
        echo "  ./run_test_cases.sh              # run using stdin"
        echo "  ./run_test_cases.sh -t <sec>     # run with time limit"
        echo "  ./run_test_cases.sh -d <folder>  # run test directory"
        exit 1
        ;;
esac
