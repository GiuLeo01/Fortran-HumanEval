# Fortran HumanEval

A **Quick and Dirty** Fortran90 adaptation of the [HumanEval](https://github.com/openai/human-eval) benchmark for evaluating Large Language Models on code generation tasks. This benchmark specifically tests the ability of language models to generate correct Fortran programs.

## Overview

The benchmark includes:

- **Automatic compilation** using gfortran
- **Test case execution** with configurable timeouts
- **Detailed result analysis** with pass@1 metrics
- **Comprehensive error categorization** (compilation errors, runtime errors, incorrect output)

  **THE BENCHMARK DOES NOT HANDLE LLM INFERENCE** but expects a well-formatted jsonl file as input.


## Quick Start

The simple evaluation pipeline:
1. **Generate responses** for each problem in the benchmark
2. **Format responses** as JSONL with `code` field
3. **Run evaluation** using the provided script

### Inference
- It is highly recommended to provide the instructions included in the system_prompt.txt file
- To generate inference with an LLM, simply iterate over each record in the benchmark (benchmark.jsonl), providing the task description, signature, and example.
  e.g.:
```python
messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{task} \n Pseudocode Signature: {signature} \n Example: {example}"}
        ]
```
  
- The content of the 'tests' field should not be used in inference, it serves for the evaluation process.


### Best Practices


- Ensure your LLM generates **complete Fortran programs** (not just functions)
- Make sure that the string in the code field of each element in the responses.jsonl file is directly executable code, watch out for ``` ``` symbols!!!
- Include proper **program structure** with 'program'/'end program' blocks
- Handle **input/output formatting** according to test specifications
- Test your pipeline with a **small subset** before full evaluation



### Prerequisites

1. **Python 3.7+** with pip
2. **gfortran compiler** installed and available in PATH

If you have problems with gfortran installation on Windows, use WSL.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fortran-humaneval.git
cd fortran-humaneval
```

2. Install Python dependencies (only tqdm):
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
gfortran --version
```

## Usage

### Basic Evaluation

```bash
python main.py responses.jsonl benchmark.json
```

### Advanced Options

```bash
# Custom timeout (default: 120s) - timeout refers to the maximum time allowed for validation of a single task (i.e., compilation time + execution time of each test case). This prevents infinite loops.
python main.py responses.jsonl benchmark.json --timeout 60

# Save detailed results
python main.py responses.jsonl benchmark.json --output detailed_results.json
```

### Input Format

#### Responses File (`responses.jsonl`)
Each line should contain a JSON object with the LLM-generated code:
```json
{"code": "program hello\n  write(*,*) 'Hello, World!'\nend program"}
{"code": "program calculate\n  integer :: result\n  result = 2 + 2\n  write(*,*) result\nend program"}
```

#### Benchmark File (`benchmark.json`) (Should not be changed unless you want to use the same format to adapt other benchmarks)
Array of programming tasks with signatures, examples and test cases:
```json
[
  {
    "task": "Write a Fortran90 program that checks if in given array of numbers, are any two numbers closer to each other than given threshold.",
    "signature": "bool has_close_elements(int numbers_len, float[] numbers, float threshold)",
    "example": "Input: 3 \n 1.0 2.0 3.0 \n 0.5 | Output: false",
    "tests": [
      {
        "input": "6 \n 1.0 2.0 3.9 4.0 5.0 2.2 \n 0.3",
        "output": true
      },
      {
        "input": "6 \n 1.0 2.0 3.9 4.0 5.0 2.2 \n 0.05",
        "output": false
      },
      {
        "input": "5 \n 1.0 2.0 5.9 4.0 5.0 \n 0.95",
        "output": true
      },
      {
        "input": "5 \n 1.0 2.0 5.9 4.0 5.0 \n 0.8",
        "output": false
      },
      {
        "input": "6 \n 1.0 2.0 3.0 4.0 5.0 2.0 \n 0.1",
        "output": true
      },
      {
        "input": "5 \n 1.1 2.2 3.1 4.1 5.1 \n 1.0",
        "output": true
      },
      {
        "input": "5 \n 1.1 2.2 3.1 4.1 5.1 \n 0.5",
        "output": false
      }
    ]
  }
]
```

## Output Metrics

- **Pass@1**: Percentage of problems solved correctly on the first attempt
- **Compilation Errors**: Programs that failed to compile
- **Runtime Errors**: Programs that compiled but crashed during execution
- **Incorrect Output**: Programs that ran but produced wrong results
- **Exceptions**: Unexpected errors during evaluation


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI** for the original [HumanEval](https://github.com/openai/human-eval) benchmark
- **GNU Fortran** community for the 'gfortran' compiler

## Citation

If you use this benchmark in your research, please cite:

```bibtex
@misc{fortran-humaneval,
  title={Fortran HumanEval: A Benchmark for Evaluating LLMs on Fortran Code Generation},
  author={Giulio Leonardi},
  year={2025},
  url={https://github.com/GiuLeo01/fortran-humaneval}
}
```

---

**Note**: This benchmark is designed for research purposes to evaluate and improve language models' capabilities in Fortran programming. Results should be interpreted in the context of the specific test cases and evaluation methodology used.
