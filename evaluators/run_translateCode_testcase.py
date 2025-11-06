# run_translateCode_testcase.py

import os
import json
import subprocess
import shutil
import tempfile
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSLATED_DIR = os.path.join(PROJECT_ROOT, "translated")
RESULTS_FILE = os.path.join(PROJECT_ROOT, "results", "results.json")

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
def save_results(model_name, data):
    results_dir = os.path.join(PROJECT_ROOT, "results")
    os.makedirs(results_dir, exist_ok=True)

    output_file = os.path.join(results_dir, "translated_results.json")

    # Load existing results if present
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            all_results = json.load(f)
    else:
        all_results = {}

    # Add/overwrite this model's results
    all_results[model_name] = data

    # Save back to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)


def prepare_java_file(java_file):
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
    return java_file, None
def run_java(java_file, input_data, as_args=False):
    java_file, temp_dir = prepare_java_file(java_file)
    class_name = os.path.splitext(os.path.basename(java_file))[0]

    compile_proc = subprocess.run(
        ["javac", java_file],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
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
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3
            )
        else:
            run_proc = subprocess.run(
                ["java", "-cp", os.path.dirname(java_file), class_name],
                input=input_str, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3
            )
    except subprocess.TimeoutExpired:
        if temp_dir:
            shutil.rmtree(temp_dir)
        return "", "[TIMEOUT]"

    if temp_dir:
        shutil.rmtree(temp_dir)

    return run_proc.stdout.strip(), run_proc.stderr.strip()


def run_python(python_file, input_data, as_args=False):
    input_str = input_data.strip() + "\n"
    try:
        if as_args:
            args_list = input_str.strip().split()
            proc = subprocess.run(
                ["python", python_file] + args_list,
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3
            )
        else:
            proc = subprocess.run(
                ["python", python_file],
                input=input_str, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3
            )
    except subprocess.TimeoutExpired:
        return "", "[TIMEOUT]"
    return proc.stdout.strip(), proc.stderr.strip()


def detect_input_mode(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    if "sys.argv[" in code or "args[" in code:
        return "args"
    return "stdin"

if __name__ == "__main__":
    original_results = load_results()
    if not original_results:
        print("[ERROR] results.json not found or empty.")
        exit(1)

    for model_name in os.listdir(TRANSLATED_DIR):
        model_path = os.path.join(TRANSLATED_DIR, model_name)
        if not os.path.isdir(model_path):
            continue

        print(f"\n=== Running tests for model: {model_name} ===")
        model_results = {}

        for prog_file in os.listdir(model_path):
            if not prog_file.endswith((".py", ".java")):
                continue

            prog_name = os.path.splitext(prog_file)[0]
            if prog_name not in original_results:
                print(f"[SKIP] No test cases for {prog_file} in results.json")
                continue

            file_path = os.path.join(model_path, prog_file)
            mode = detect_input_mode(file_path)
            as_args = (mode == "args")

            test_cases = original_results[prog_name]
            prog_outputs = []

            for case in test_cases:
                input_data = case["input"]
                if file_path.endswith(".java"):
                    out, err = run_java(file_path, input_data, as_args)
                else:
                    out, err = run_python(file_path, input_data, as_args)

                prog_outputs.append({
                    "input": input_data,
                    "expected_output": case["output"],
                    "expected_error": case["error"],
                    "translated_output": out,
                    "translated_error": err
                })

            model_results[prog_name] = prog_outputs

        save_results(model_name, model_results)
        print(f"[SAVED] Translated test results for {model_name}")
