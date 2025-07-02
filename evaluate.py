from tqdm import tqdm
import signal
import subprocess
import subprocess
import os
import tempfile
import re
import platform






# timeout exception
class TimeoutException(Exception):
    pass

# signal handler
def timeout_handler(signum, frame):
    raise TimeoutException()

# register the signal handler
signal.signal(signal.SIGALRM, timeout_handler)


def compile_fortran(fortran_code:str):
    """
    Function that compiles a fortran90 program using the gfortran compiler.
    In case of success, returns the executable and its path
    """
    # creation of the temporary f90 file
    with tempfile.NamedTemporaryFile(suffix=".f90", delete=False, mode='w') as f:
        f.write(fortran_code)
        fortran_path = f.name

    exe_suffix = ".exe" if platform.system() == "Windows" else ""
    executable = fortran_path.replace(".f90", exe_suffix)
    
    compile_cmd = ["gfortran", "-o", executable, fortran_path]

    # file compilation
    try:
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return executable, fortran_path
    except subprocess.CalledProcessError as e:
        return None, fortran_path, e.stderr.decode()
    


def parse_response(output: str) -> list[str]:
    stripped = output.strip()
    if not stripped:
        return []
    return [re.sub(r'\[s\]', r' ', st) for st in stripped.split()]

def parse_bool(s):
    """
    Function that parses booleans given as output by the fortran program
    """
    s = s.strip().lower()
    if s in (".true.", "true", "t", "1"): return True
    if s in (".false.", "false", "f", "0"): return False
    raise ValueError(f"Not a boolean: {s}")

def equality(x, y, float_tol=1e-2):
    """function that verifies equality between single elements of the program output and expected output"""
    if x == '' and y == []:
        return True

    try:
        if isinstance(y, bool):
            return parse_bool(x) == y
    except:
        pass

    try:
        if abs(float(x) - float(y)) < float_tol:
            return True
    except:
        pass

    return str(x) == str(y)


def program_evaluation(fortran_code: str, test_cases: list):
    """
    Function that executes the correctness evaluation of a fortran program 
    through a battery of tests, compiling the code only once.
    """
    # Code compilation (only once)
    compile_result = compile_fortran(fortran_code)
    executable, source_file = compile_result[0], compile_result[1]
    
    # If compilation fails
    if not executable:
        stderr_msg = compile_result[2] if len(compile_result) > 2 else "Unknown compile error"
        if os.path.exists(source_file):
            os.remove(source_file)
        return 0, ('compile_err', stderr_msg)
    
    try:
        # Executes all test cases
        for i, test_case in enumerate(test_cases):
            input_data = test_case['input']
            expected_output = test_case['output']
            
            # Executes the single test
            result = run_program(executable, input_data, expected_output)
            
            # If a test fails, immediately returns the result
            if result[0] == 0:
                return result
        
        # If all tests passed
        return 1, ('ok', 'All tests passed')
        
    finally:
        # Cleanup of temporary files
        if os.path.exists(executable):
            os.remove(executable)
        if os.path.exists(source_file):
            os.remove(source_file)


def run_program(executable, input_data="", expected_output=None):
    """
    Executes the executable program with input_data, parses its output and compares it
    with expected_output. Returns (score, (status, details)) where:
      - score: 1 if OK, 0 otherwise
      - status: 'ok', 'ineq', 'runtime_err' or 'exception'
      - details: in case of 'ok' or 'ineq', (raw_output, expected_output)
                 for 'runtime_err', the stderr message
                 for 'exception', the exception string
    """
    def normalize(x):
        # helps to treat scalars and lists in the same way
        if expected_output is None:
            return []
        return x if isinstance(x, list) else [x]

    try:
        # execution
        proc = subprocess.run(
            [executable],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )

        # runtime error check
        if proc.stderr:
            return 0, ('runtime_err', proc.stderr)
        
        if proc.stdout.strip() == str(expected_output).strip():
            return 1, ('ok', (proc.stdout.strip(), expected_output))

        raw = proc.stdout.strip()
        # parsing of the output
        actual = parse_response(raw)
        exp = expected_output if expected_output is not None else []
        
        # normalize into lists
        actual_list = normalize(actual)
        expected_list = normalize(exp)

        # if different lengths, it's inequality
        if len(actual_list) != len(expected_list):
            return 0, ('ineq', (raw, exp))

        # element by element comparison
        for a, b in zip(actual_list, expected_list):
            try:
                if not equality(a, b):
                    return 0, ('ineq', (raw, exp))
            except Exception:
                return 0, ('ineq', (raw, exp))

        # ok
        return 1, ('ok', (raw, exp))

    except Exception as e:
        return 0, ('exception', str(e))



def evaluation(benchmark, inference, execution_time_limit=120):
    c = {
        'ineq': 0,
        'runtime_err': 0,
        'ok': 0,
        'exception': 0,
        'compile_err': 0,
        'ids': []
    }
    logs = {
        'ineq': [],
        'runtime_err': [],
        'ok': [],
        'exception': [],
        'compile_err': []
    }

    for i in tqdm(range(len(inference))):
        bench = benchmark[i]
        code = inference[i]['code']
        test_cases = bench['tests']
        
        try:
            signal.alarm(execution_time_limit)
            # Executes all tests for the current program
            result = program_evaluation(code, test_cases)
            signal.alarm(0)
        except TimeoutException:
            result = (0, ('runtime_err', 'Timeout exceeded'))
            signal.alarm(0)
        
        # If all tests passed, result[0] will be 1, otherwise 0
        if result[0] == 1:
            c['ok'] += 1
        else:
            c[result[1][0]] += 1
            c['ids'].append(i)
        
        logs[result[1][0]].append(result[1][1])
    
    return c, logs