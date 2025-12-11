import matplotlib.pyplot as plt
import csv

# Read CSV file
test_cases = []
upper_bounds = []
wills_solutions = []
nates_solutions = []
bens_exact_solutions = []

with open('n9_comparison_results.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        test_cases.append(row['test_case'])
        upper_bounds.append(int(row['upper_bound']))
        wills_solutions.append(int(row['wills_solution']))
        nates_solutions.append(int(row['nates_solution']))
        bens_exact_solutions.append(int(row['bens_exact_solution']))

# Create line graph
plt.figure(figsize=(12, 6))
plt.plot(test_cases, upper_bounds, marker='o', label='Upper Bound', linewidth=2)
plt.plot(test_cases, wills_solutions, marker='s', label="Will's Solution", linewidth=2)
plt.plot(test_cases, nates_solutions, marker='^', label="Nate's Solution", linewidth=2)
plt.plot(test_cases, bens_exact_solutions, marker='d', label="Ben's Exact Solution", linewidth=2)

# Set limits for zooming in
plt.xlim(0, len(test_cases) - 1)  # Adjust based on the number of test cases
plt.ylim(0, max(max(upper_bounds), max(wills_solutions), max(nates_solutions), max(bens_exact_solutions)) + 1)  # Adjust y-axis limit based on max values

plt.xlabel('Test Case', fontsize=12)
plt.ylabel('Path Length', fontsize=12)
plt.title('Longest Path: Approximations vs Exact Solution (n=12)', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('n7_comparison.png', dpi=300)
plt.show()

print(f"Graph saved as n7_comparison.png")
