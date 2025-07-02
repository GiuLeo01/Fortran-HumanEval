import json

def print_results(counters):
    """Print evaluation results in a readable format."""
    total = sum(counters[key] for key in ['ok', 'ineq', 'runtime_err', 'exception', 'compile_err'])
    
    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    
    print(f"Total tests executed: {total}")
    print(f"Tests passed (pass@1): {counters['ok']} ({counters['ok']/total*100:.1f}%)")
    print(f"Compilation errors: {counters['compile_err']} ({counters['compile_err']/total*100:.1f}%)")
    print(f"Runtime errors: {counters['runtime_err']} ({counters['runtime_err']/total*100:.1f}%)")
    print(f"Incorrect output: {counters['ineq']} ({counters['ineq']/total*100:.1f}%)")
    print(f"Exceptions: {counters['exception']} ({counters['exception']/total*100:.1f}%)")
    
    print("\n" + "="*50)


def save_detailed_results(counters, logs, output_file):
    """Save results to a JSON file."""
    results = {
        'summary': counters,
        'detailed_logs': logs
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Detailed results saved to: {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")