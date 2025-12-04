import subprocess
import re
import os
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime

# Configuration
SELF_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
BASH_SCRIPT = SELF_PATH / "../approx_solution_2/test_cases/run_test_cases.sh"
APPROX2_LOG = SELF_PATH / "../approx_solution_2/test_cases/test_output.log"
EXACT_LOG = SELF_PATH / "../exact_solution/test_result_data/test_data.log"
OUTPUT_DIR = SELF_PATH / "thread_analysis_results"

# Thread counts to test
THREAD_COUNTS = range(1, 17)  # Test from 1 to 16 threads
T_ARG = 1 # arg -t to pass to the program

def parse_approx2_log(filename):
    """Parse the approximation algorithm log format."""
    results = {}
    with open(filename, 'r') as f:
        content = f.read()
    
    entries = content.strip().split('=============================================')
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        file_match = re.search(r'File:\s*(.+)', entry)
        if not file_match:
            continue
        test_file = file_match.group(1).strip()
        
        time_match = re.search(r'Elapsed:\s*([\d.]+)\s*seconds', entry)
        elapsed = float(time_match.group(1)) if time_match else None
        
        length_match = re.search(r'Longest path found:\s*(\d+)', entry)
        path_length = int(length_match.group(1)) if length_match else None
        
        path_match = re.search(r'Path:\s*(.+)', entry)
        path = path_match.group(1).strip() if path_match else None
        
        results[test_file] = {
            'length': path_length,
            'path': path,
            'time': elapsed
        }
    
    return results

def parse_exact_log(filename):
    """Parse the exact solver log format."""
    results = {}
    with open(filename, 'r') as f:
        content = f.read()
    
    entries = content.strip().split('===============================')
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        file_match = re.search(r'File:\stest_cases\/*(.+)', entry)
        if not file_match:
            continue
        test_file = file_match.group(1).strip()
        
        time_match = re.search(r'Elapsed:\s*([\d.]+)\s*seconds', entry)
        elapsed = float(time_match.group(1)) if time_match else None
        
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

def run_test_with_threads(thread_count):
    """Run the bash script with specified thread count."""
    print(f"\n{'='*60}")
    print(f"Running test with {thread_count} threads...")
    print(f"{'='*60}")
    
    try:
        # On Windows, need to run through bash (Git Bash, WSL, or similar)
        # Try different bash executables in order of preference
        bash_executables = [
            "bash",  # If bash is in PATH
            "C:\\Program Files\\Git\\bin\\bash.exe",  # Git Bash default location
            "wsl",  # Windows Subsystem for Linux
        ]
        
        bash_cmd = None
        for bash_exe in bash_executables:
            try:
                # Test if this bash executable works
                test_result = subprocess.run([bash_exe, "--version"], 
                                            capture_output=True, 
                                            timeout=5)
                if test_result.returncode == 0:
                    bash_cmd = bash_exe
                    print(f"Using bash: {bash_exe}")
                    break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        if bash_cmd is None:
            print("Error: Could not find bash executable.")
            print("Please install Git Bash or WSL, or ensure bash is in your PATH")
            return None
        
        # Build command with bash interpreter
        cmd = [bash_cmd, str(BASH_SCRIPT), "-t", str(T_ARG), "-p", str(thread_count)]
        print(f"Executing: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        print(f"Exit code: {result.returncode}")
        
        if result.stdout:
            print(f"stdout preview: {result.stdout[:200]}")
        
        if result.returncode != 0:
            print(f"Warning: Script returned non-zero exit code: {result.returncode}")
            print(f"stderr: {result.stderr}")
        
        # Parse the log file
        if APPROX2_LOG.exists():
            results = parse_approx2_log(APPROX2_LOG)
            print(f"Successfully parsed {len(results)} test results")
            return results
        else:
            print(f"Error: Log file not found at {APPROX2_LOG}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"Error: Test with {thread_count} threads timed out")
        return None
    except FileNotFoundError:
        print(f"Error: Bash script not found at {BASH_SCRIPT}")
        print("Please check the BASH_SCRIPT path in the configuration")
        return None
    except Exception as e:
        print(f"Error running test with {thread_count} threads: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_results(all_results, exact_results):
    """Analyze results across different thread counts."""
    
    # Get all test files
    test_files = set()
    for results in all_results.values():
        if results:
            test_files.update(results.keys())
    
    analysis = {
        'per_thread': {},
        'per_file': defaultdict(lambda: {'threads': [], 'lengths': [], 'accuracies': []}),
        'summary': {}
    }
    
    # Analyze per thread count
    for thread_count, results in all_results.items():
        if not results:
            continue
            
        total_accuracy = 0
        count = 0
        optimal_count = 0
        
        for test_file, result in results.items():
            if result['length'] is not None and test_file in exact_results:
                exact_len = exact_results[test_file]['length']
                if exact_len:
                    accuracy = (result['length'] / exact_len) * 100
                    total_accuracy += accuracy
                    count += 1
                    
                    if result['length'] == exact_len:
                        optimal_count += 1
                    
                    # Store per-file data
                    analysis['per_file'][test_file]['threads'].append(thread_count)
                    analysis['per_file'][test_file]['lengths'].append(result['length'])
                    analysis['per_file'][test_file]['accuracies'].append(accuracy)
        
        analysis['per_thread'][thread_count] = {
            'avg_accuracy': total_accuracy / count if count > 0 else 0,
            'optimal_count': optimal_count,
            'total_tests': len(results)
        }
    
    return analysis

def create_visualizations(analysis, output_dir):
    """Create visualization plots."""
    if not analysis['per_thread']:
        print("\nSkipping visualizations - no data to plot")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    threads = sorted(analysis['per_thread'].keys())
    avg_accuracies = [analysis['per_thread'][t]['avg_accuracy'] for t in threads]
    optimal_counts = [analysis['per_thread'][t]['optimal_count'] for t in threads]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Average Accuracy
    ax1.plot(threads, avg_accuracies, marker='o', color='red', linewidth=2, markersize=8)
    ax1.set_xlabel('Thread Count', fontsize=12)
    ax1.set_ylabel('Average Accuracy (%)', fontsize=12)
    ax1.set_title('Average Accuracy vs Thread Count', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(threads)
    if avg_accuracies:
        ax1.set_ylim([min(avg_accuracies) - 5, 100])
    
    # 2. Optimal Solutions Count
    ax2.bar(threads, optimal_counts, color='green', alpha=0.7)
    ax2.set_xlabel('Thread Count', fontsize=12)
    ax2.set_ylabel('Number of Optimal Solutions', fontsize=12)
    ax2.set_title('Optimal Solutions Found vs Thread Count', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_xticks(threads)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'thread_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved analysis plot to {output_dir / 'thread_analysis.png'}")
    
    plt.close('all')

def print_summary(analysis):
    """Print summary statistics."""
    print("\n" + "="*80)
    print("THREAD ANALYSIS SUMMARY")
    print("="*80)
    
    if not analysis['per_thread']:
        print("\nNo successful test runs to analyze.")
        print("Please check:")
        print("  1. Bash script path is correct")
        print("  2. Bash script has execute permissions")
        print("  3. Log file path is correct")
        print("  4. Tests are completing successfully")
        return
    
    print(f"\n{'Threads':<10} {'Avg Accuracy (%)':<20} {'Optimal Solutions':<20} {'Total Tests':<15}")
    print("-"*80)
    
    for thread_count in sorted(analysis['per_thread'].keys()):
        stats = analysis['per_thread'][thread_count]
        print(f"{thread_count:<10} "
              f"{stats['avg_accuracy']:<20.2f} "
              f"{stats['optimal_count']:<20} "
              f"{stats['total_tests']:<15}")
    
    # Find best configurations
    print("\n" + "="*80)
    print("BEST CONFIGURATIONS")
    print("="*80)
    
    best_accuracy_thread = max(analysis['per_thread'].items(), 
                               key=lambda x: x[1]['avg_accuracy'])
    best_optimal_thread = max(analysis['per_thread'].items(), 
                             key=lambda x: x[1]['optimal_count'])
    
    print(f"\nBest Average Accuracy: {best_accuracy_thread[0]} threads "
          f"({best_accuracy_thread[1]['avg_accuracy']:.2f}%)")
    print(f"Most Optimal Solutions: {best_optimal_thread[0]} threads "
          f"({best_optimal_thread[1]['optimal_count']} optimal)")
    
    print("\n" + "="*80)

def save_results_json(all_results, analysis, output_dir):
    """Save detailed results to JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'thread_counts_tested': list(THREAD_COUNTS),
        'raw_results': {str(k): v for k, v in all_results.items()},
        'analysis': {
            'per_thread': {str(k): v for k, v in analysis['per_thread'].items()},
            'per_file': {k: dict(v) for k, v in analysis['per_file'].items()}
        }
    }
    
    output_file = output_dir / 'results.json'
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nSaved detailed results to {output_file}")

def main():
    """Main execution function."""
    print("="*80)
    print("MULTI-THREADED APPROXIMATION ANALYSIS")
    print("="*80)
    print(f"Testing thread counts: {list(THREAD_COUNTS)}")
    print(f"Bash script: {BASH_SCRIPT}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Check if bash script exists
    if not BASH_SCRIPT.exists():
        print(f"\nError: Bash script not found at {BASH_SCRIPT}")
        print("Please update the BASH_SCRIPT path in the configuration section.")
        return
    
    # Load exact results for comparison
    print("\nLoading exact results for comparison...")
    exact_results = parse_exact_log(EXACT_LOG)
    print(f"Loaded {len(exact_results)} exact results")
    
    # Run tests with different thread counts
    all_results = {}
    for thread_count in THREAD_COUNTS:
        results = run_test_with_threads(thread_count)
        all_results[thread_count] = results
    
    # Analyze results
    print("\nAnalyzing results...")
    analysis = analyze_results(all_results, exact_results)
    
    # Print summary
    print_summary(analysis)
    
    # Create visualizations
    print("\nCreating visualizations...")
    create_visualizations(analysis, OUTPUT_DIR)
    
    # Save detailed results
    print("\nSaving detailed results...")
    save_results_json(all_results, analysis, OUTPUT_DIR)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nResults saved to: {OUTPUT_DIR}")
    print(f"- Analysis plot: thread_analysis.png")
    print(f"- Detailed data: results.json")

if __name__ == "__main__":
    main()