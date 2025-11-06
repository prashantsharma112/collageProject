

# run_sourceCode_testcase.py
import subprocess
import sys
import json
import os
import re
import shutil
import tempfile

# Import from your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from evaluators.test_case_generator import (
    detect_input_count_from_code,
    generate_edge_cases,
    detect_input_types_from_code
)

INPUT_PROGRAM_DIR = os.path.join(os.path.dirname(__file__), "..", "input_program")
# Path to "results" directory in project root
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)  # Create folder if it doesn't exist

# Path to JSON file inside "results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.json")

def load_results():
    """Load results.json if exists, else return empty dict."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_results(data):
    """Save the updated results to results.json."""
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def prepare_java_file(java_file):
    """Read .java file, detect public class name, and save a temp copy with correct filename."""
    with open(java_file, "r", encoding="utf-8") as f:
        code = f.read()

    match = re.search(r"public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)", code)
    if match:
        class_name = match.group(1)
        temp_dir = tempfile.mkdtemp()
        correct_path = os.path.join(temp_dir, f"{class_name}.java")
        with open(correct_path, "w", encoding="utf-8") as f:
            f.write(code)
        return correct_path, temp_dir
    else:
        return java_file, None


def run_java(java_file, input_data, as_args):
    java_file, temp_dir = prepare_java_file(java_file)
    class_name = os.path.splitext(os.path.basename(java_file))[0]

    compile_proc = subprocess.run(["javac", java_file], capture_output=True, text=True)
    if compile_proc.returncode != 0:
        if temp_dir:
            shutil.rmtree(temp_dir)
        return "", compile_proc.stderr.strip()

    input_str = input_data.strip() + "\n"

    try:
        if as_args:
            args_list = input_str.strip().split()
            run_proc = subprocess.run(
                ["java", "-cp", os.path.dirname(java_file), class_name] + args_list,
                capture_output=True, text=True, timeout=3
            )
        else:
            run_proc = subprocess.run(
                ["java", "-cp", os.path.dirname(java_file), class_name],
                input=input_str, capture_output=True, text=True, timeout=3
            )
    except subprocess.TimeoutExpired:
        if temp_dir:
            shutil.rmtree(temp_dir)
        return "", "[TIMEOUT] Program took too long to respond."

    if temp_dir:
        shutil.rmtree(temp_dir)

    return run_proc.stdout.strip(), run_proc.stderr.strip()


def run_python(python_file, input_data, as_args):
    input_str = input_data.strip() + "\n"

    try:
        if as_args:
            args_list = input_str.strip().split()
            proc = subprocess.run(["python", python_file] + args_list,
                                  capture_output=True, text=True, timeout=3)
        else:
            proc = subprocess.run(["python", python_file],
                                  input=input_str, capture_output=True, text=True, timeout=3)
    except subprocess.TimeoutExpired:
        return "", "[TIMEOUT] Program took too long to respond."

    return proc.stdout.strip(), proc.stderr.strip()


def detect_input_mode(file_path):
    """Detect whether program uses stdin or command-line args."""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    if "sys.argv[" in code or "args[" in code:
        return "args"
    return "stdin"


if __name__ == "__main__":
    results_data = load_results()

    program_files = [f for f in os.listdir(INPUT_PROGRAM_DIR) if f.endswith((".java", ".py"))]
    if not program_files:
        print("No Java or Python program found in input_program/")
        sys.exit(1)

    try:
        num_cases = int(sys.argv[1])
    except (IndexError, ValueError):
        num_cases = 5  # default if no argument passed

    for program_file in program_files:
        file_path = os.path.join(INPUT_PROGRAM_DIR, program_file)
        program_name = os.path.splitext(program_file)[0]

        print("\n" + "=" * 50)
        print(f"🔍 Testing program: {file_path}")

        # Skip if program already exists in results.json
        if program_name in results_data:
            print(f"[SKIP] Test cases already generated for {program_file}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        lang = "java" if file_path.endswith(".java") else "python"
        input_count = detect_input_count_from_code(code, lang)
        detected_type = detect_input_types_from_code(code, lang)
        detected_types = [detected_type]

        print(f"[INFO] Detected {input_count} inputs for this program.")
        print(f"[INFO] Detected supported data types: {detected_types}")

        program_results = []
        for dtype in detected_types:
            print(f"\n[INFO] Generating test cases for data type: {dtype}")
            test_inputs = generate_edge_cases(input_type=dtype, count=num_cases, num_inputs=input_count)
            print(f"[DEBUG] Generated Test Inputs: {test_inputs}")

            mode = detect_input_mode(file_path)
            as_args = (mode == "args")

            for test_input in test_inputs:
                if file_path.endswith(".java"):
                    out, err = run_java(file_path, test_input, as_args)
                else:
                    out, err = run_python(file_path, test_input, as_args)

                program_results.append({
                    "input": test_input.strip(),
                    "output": out,
                    "error": err
                })

        # Store results in main JSON
        results_data[program_name] = program_results
        save_results(results_data)

        print(f"[SAVED] Results for {program_file} stored in results.json")
