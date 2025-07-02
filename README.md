# Fortran HumanEval

A **Quick and Dirty** Fortran90 adaptation of the [HumanEval](https://github.com/openai/human-eval) benchmark for evaluating Large Language Models (LLMs) on code generation tasks. This benchmark specifically tests the ability of language models to generate correct Fortran programs.

## Overview

The benchmark includes:

- **Automatic compilation** using gfortran
- **Test case execution** with configurable timeouts
- **Detailed result analysis** with pass@1 metrics
- **Comprehensive error categorization** (compilation errors, runtime errors, incorrect output)

  **IL BENCHMARK NON GESTISCE L'INFERENZA DEL LLM** ma si aspetta in input un file jsonl ben formattato.


## Quick Start

The simple evaluation pipeline:
1. **Generate responses** for each problem in the benchmark
2. **Format responses** as JSONL with `code` field
3. **Run evaluation** using the provided script

### Inference
- è altamente consigliato fornire le istruzioni comprese nel file system_prompt.txt
- 


### Best Practices



- Ensure your LLM generates **complete Fortran programs** (not just functions)
- Include proper **program structure** with `program`/`end program` blocks
- Handle **input/output formatting** according to test specifications
- Test your pipeline with a **small subset** before full evaluation



### Prerequisites

1. **Python 3.7+** with pip
2. **gfortran compiler** installed and available in PATH

Se avete problemi con l'installazione di gfortran in Windows, usate WSL.

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
# Custom timeout (default: 120s)
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

#### Benchmark File (`benchmark.json`) (Non va cambiato a meno che vogliate usare lo stesso formato per adattare altri benchmark)
Array of test cases with input/output specifications:
```json
[
  {
    "task": "Hello World",
    "tests": [
      {
        "input": "",
        "output": "Hello, World!"
      }
    ]
  }
]
```

## 📊 Output Metrics

- **Pass@1**: Percentage of problems solved correctly on the first attempt
- **Compilation Errors**: Programs that failed to compile
- **Runtime Errors**: Programs that compiled but crashed during execution
- **Incorrect Output**: Programs that ran but produced wrong results
- **Exceptions**: Unexpected errors during evaluation

## 🏗️ Architecture


### Evaluation Flow

1. Load benchmark and responses from JSON/JSONL files
2. Validate input format and file structure
3. Compile each Fortran program using gfortran
4. Execute compiled programs with test inputs
5. Compare outputs against expected results
6. Categorize results and generate comprehensive reports


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for the original [HumanEval](https://github.com/openai/human-eval) benchmark
- **GNU Fortran** community for the `gfortran` compiler
- **Contributors** who help improve this evaluation framework

## 📚 Citation

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
