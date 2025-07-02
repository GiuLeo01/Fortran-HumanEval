#!/usr/bin/env python3
import json
import argparse
import sys
from pathlib import Path


from evaluate import evaluation
from utils import *


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate LLM responses on Fortran HumanEval benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python main.py responses.json benchmark.json
  python main.py responses.json benchmark.json --timeout 60
  python main.py responses.json benchmark.json --output results.json
        """
    )
    

    # Command line args
    parser.add_argument(
        'responses_file',
        help='Path to JSON file containing LLM responses'
    )
    
    parser.add_argument(
        'benchmark_file', 
        help='Path to JSON file containing benchmark test cases'
    )
    
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=120,
        help='Timeout in seconds for each program execution (default: 120)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file to save detailed results (optional)'
    )
    
    args = parser.parse_args()
    
    # Check if files exist
    if not Path(args.responses_file).exists():
        print(f"Error: Response file not found: {args.responses_file}")
        sys.exit(1)
        
    if not Path(args.benchmark_file).exists():
        print(f"Error: Benchmark file not found: {args.benchmark_file}")
        sys.exit(1)


    # Benchmark file loading
    try:
        benchmark = []
        with open(args.benchmark_file, 'r') as file:
            benchmark = json.load(file)
    except Exception as e:
        print('Error during the benchmark jsonl loading')
        sys.exit(1)

    # Inference file loading
    try:
        inference = []
        with open(args.responses_file, 'r') as file:
            for line in file:
                inference.append(json.loads(line))
    except Exception as e:
        print('Error during the inference jsonl loading')
        sys.exit(1)

    
    # Verify data structure
    if not isinstance(inference, list):
        print("Error: Response file must contain a list")
        sys.exit(1)
        
    if not isinstance(benchmark, list):
        print("Error: Benchmark file must contain a list")
        sys.exit(1)
        
    if len(inference) != len(benchmark):
        print(f"Error: Number of responses ({len(inference)}) differs from number of benchmark tests ({len(benchmark)})")
        sys.exit(1)
    
    # Run evaluation
    print(f"Starting Fortran HumanEval evaluation")
    
    try:
        counters, logs = evaluation(benchmark, inference, args.timeout)
    except KeyboardInterrupt:
        print("\nEvaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during evaluation: {e}")
        sys.exit(1)
    
    # Print results
    print_results(counters)
    
    # Save detailed results if requested
    if args.output:
        save_detailed_results(counters, logs, args.output)


if __name__ == "__main__":
    main()