#!/usr/bin/env python3
"""Compare actual test results against expected results."""

# Read expected results
expected_file = "/Users/ellonamacmillan/Documents/Fall 25'/cs452/longest_path_452f25/reduced_solution/expected_results.txt"
with open(expected_file, 'r') as f:
    expected_lines = f.readlines()

# Parse expected results into a dict
expected = {}
for line in expected_lines:
    line = line.strip()
    if line:
        parts = line.split(': ')
        if len(parts) == 2:
            test_name = parts[0]
            result = parts[1]
            expected[test_name] = result

# Read actual results
results_file = "/Users/ellonamacmillan/Documents/Fall 25'/cs452/longest_path_452f25/reduced_solution/results.txt"
with open(results_file, 'r') as f:
    results_lines = f.readlines()

# Parse actual results - extract HAM/NO HAM lines only
actual = {}
test_counter = 1
for line in results_lines:
    line = line.strip()
    if line.startswith("HAM FOUND"):
        test_name = f"t{test_counter:02d}.txt"
        actual[test_name] = "HAM"
        test_counter += 1
    elif line.startswith("NO HAM"):
        test_name = f"t{test_counter:02d}.txt"
        actual[test_name] = "NO HAM"
        test_counter += 1

# Compare results
print("=" * 80)
print("TEST COMPARISON REPORT")
print("=" * 80)

mismatches = []
matches = 0

for i in range(1, 51):
    test_name = f"t{i:02d}.txt"
    expected_result = expected.get(test_name, "UNKNOWN")
    actual_result = actual.get(test_name, "MISSING")

    if expected_result == actual_result:
        matches += 1
        status = "✓ PASS"
    else:
        status = "✗ FAIL"
        mismatches.append((test_name, expected_result, actual_result))

    print(f"{test_name}: {status:8} | Expected: {expected_result:7} | Actual: {actual_result}")

print("=" * 80)
print(f"SUMMARY: {matches} / 50 tests passed")
print("=" * 80)

if mismatches:
    print("\nMISMATCHES:")
    for test_name, exp, act in mismatches:
        print(f"  {test_name}: Expected {exp} but got {act}")
else:
    print("\n✓ All tests passed!")
