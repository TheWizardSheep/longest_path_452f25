SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_INTERPRETER="python"
PYTHON_SCRIPT="$SCRIPT_DIR/../approximation.py"

echo "Beginning test (run-all mode):"

trap '' SIGINT   # ignore Ctrl-C in the shell while starting
$PYTHON_INTERPRETER "$PYTHON_SCRIPT" --run-all "$@"
trap - SIGINT    # restore normal Ctrl-C handling