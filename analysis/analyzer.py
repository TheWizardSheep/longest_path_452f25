import re
import argparse
import os
from pathlib import Path
from collections import defaultdict

SELF_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
EXACT_LOG = SELF_PATH/"../exact_solution/test_output.log"
APPROX2_LOG = SELF_PATH/"../approx_solution_2/test_cases/test_output.log"

def parse_exact_log(filename):
    """Parse the exact solver log format."""
    results = {}
    with open(filename, 'r') as f:
        content = f.read()
    
    # Split by separator
    entries = content.strip().split('===============================')
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        # Extract file name
        file_match = re.search(r'File:\stest_cases\/*(.+)', entry)
        if not file_match:
            continue
        test_file = file_match.group(1).strip()
        
        # Extract elapsed time
        time_match = re.search(r'Elapsed:\s*([\d.]+)\s*seconds', entry)
        elapsed = float(time_match.group(1)) if time_match else None
        
        # Extract output (path length and path)
        output_match = re.search(r'Output:\s*\n(\d+)\s*\n(.+)', entry)
        if output_match:
            path_length = int(output_match.group(1))
            path = output_match.group(2).strip()
        else:
            path_length = None
            path = None
        
        results[test_file] = {
            'length': path_length,
            'path': path,
            'time': elapsed
        }
    
    return results

def parse_approx2_log(filename):
    """Parse the approximation algorithm log format."""
    results = {}
    with open(filename, 'r') as f:
        content = f.read()
    
    # Split by separator (different separator for approx log)
    entries = content.strip().split('=============================================')
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        # Extract file name
        file_match = re.search(r'File:\s*(.+)', entry)
        if not file_match:
            continue
        test_file = file_match.group(1).strip()
        
        # Extract elapsed time
        time_match = re.search(r'Elapsed:\s*([\d.]+)\s*seconds', entry)
        elapsed = float(time_match.group(1)) if time_match else None
        
        # Extract path length (format: "Longest path found: 67")
        length_match = re.search(r'Longest path found:\s*(\d+)', entry)
        path_length = int(length_match.group(1)) if length_match else None
        
        # Extract path (format: "Path: a->b->c")
        path_match = re.search(r'Path:\s*(.+)', entry)
        path = path_match.group(1).strip() if path_match else None
        
        results[test_file] = {
            'length': path_length,
            'path': path,
            'time': elapsed
        }
    
    return results

def compare_logs(exact_results, approx_results):
    """Compare exact and approximation results."""
    all_files = set(exact_results.keys()) | set(approx_results.keys())
    
    stats = {
        'total': 0,
        'optimal': 0,
        'suboptimal': 0,
        'missing_exact': 0,
        'missing_approx': 0,
        'accuracy_sum': 0.0,
        'time_exact_sum': 0.0,
        'time_approx_sum': 0.0
    }
    
    comparison = []
    
    for test_file in sorted(all_files):
        exact = exact_results.get(test_file)
        approx = approx_results.get(test_file)
        
        if not exact:
            stats['missing_exact'] += 1
            continue
        if not approx:
            stats['missing_approx'] += 1
            continue
        
        stats['total'] += 1
        
        exact_len = exact['length']
        approx_len = approx['length']
        exact_time = exact['time']
        approx_time = approx['time']
        
        if exact_len and approx_len:
            accuracy = (approx_len / exact_len) * 100 if exact_len > 0 else 100.0
            stats['accuracy_sum'] += accuracy
            
            if approx_len == exact_len:
                stats['optimal'] += 1
                status = "OPTIMAL"
            else:
                stats['suboptimal'] += 1
                status = "SUBOPTIMAL"
        else:
            accuracy = None
            status = "ERROR"
        
        if exact_time:
            stats['time_exact_sum'] += exact_time
        if approx_time:
            stats['time_approx_sum'] += approx_time
        
        comparison.append({
            'file': test_file,
            'exact_len': exact_len,
            'approx_len': approx_len,
            'exact_time': exact_time,
            'approx_time': approx_time,
            'accuracy': accuracy,
            'status': status
        })
    
    return comparison, stats

def print_comparison(comparison, stats):
    """Print the comparison results."""
    print("=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)
    
    print(f"\n{'File':<40} {'Exact':<8} {'Approx':<8} {'Accuracy':<10} {'Status':<12}")
    print("-" * 80)
    
    for result in comparison:
        exact_str = str(result['exact_len']) if result['exact_len'] is not None else "N/A"
        approx_str = str(result['approx_len']) if result['approx_len'] is not None else "N/A"
        acc_str = f"{result['accuracy']:.2f}%" if result['accuracy'] is not None else "N/A"
        
        print(f"{result['file']:<40} {exact_str:<8} {approx_str:<8} {acc_str:<10} {result['status']:<12}")
    print()
    
    # Summary statistics
    print("\nSUMMARY STATISTICS")
    print("-" * 80)
    print(f"Total test cases compared: {stats['total']}")
    print(f"Optimal solutions found: {stats['optimal']} ({stats['optimal']/stats['total']*100:.1f}%)" if stats['total'] > 0 else "N/A")
    print(f"Suboptimal solutions: {stats['suboptimal']} ({stats['suboptimal']/stats['total']*100:.1f}%)" if stats['total'] > 0 else "N/A")
    
    if stats['total'] > 0:
        avg_accuracy = stats['accuracy_sum'] / stats['total']
        print(f"Average accuracy: {avg_accuracy:.2f}%")
    
    if stats['total'] > 0 and stats['time_exact_sum'] > 0:
        print(f"\nAverage time (exact): {stats['time_exact_sum']/stats['total']:.6f} seconds")
    if stats['total'] > 0 and stats['time_approx_sum'] > 0:
        print(f"Average time (approx): {stats['time_approx_sum']/stats['total']:.6f} seconds")
    
    if stats['time_exact_sum'] > 0 and stats['time_approx_sum'] > 0:
        speedup = stats['time_exact_sum'] / stats['time_approx_sum']
        print(f"Speedup factor: {speedup:.2f}x")
    
    if stats['missing_exact'] > 0:
        print(f"\nWarning: {stats['missing_exact']} files missing from exact log")
    if stats['missing_approx'] > 0:
        print(f"Warning: {stats['missing_approx']} files missing from approximation log")
    
    print("=" * 80)

if __name__ == "__main__":
    # Parse both logs
    exact_results = parse_exact_log(EXACT_LOG)
    approx_results = parse_approx2_log(APPROX2_LOG)
    
    # Compare results
    comparison, stats = compare_logs(exact_results, approx_results)
    
    # Print comparison
    print_comparison(comparison, stats)