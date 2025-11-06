
import random
import re
import os

# Get project root path (parent of 'evaluators')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "input_program")

if not os.path.exists(INPUT_DIR):
    print(f"[ERROR] Directory '{INPUT_DIR}' not found.")
    exit(1)

import re

def detect_input_types_from_code(code, lang="java"):
    types_found = []

    if lang.lower() == "java":
        lines = code.splitlines()
        skip_nextline_indexes = set()

        # Identify dummy nextLine() by scanning backwards for numeric/boolean input
        for i, line in enumerate(lines):
            if re.search(r"\.nextLine\s*\(", line):
                for back in range(i-1, -1, -1):
                    prev_line = lines[back].strip()
                    if prev_line == "" or prev_line.startswith("//") or prev_line.startswith("System.out"):
                        continue
                    if re.search(r"\.next(Int|Double|Float|Long|Short|Byte|Boolean)\s*\(", prev_line):
                        skip_nextline_indexes.add(i)
                    break

        # Match Scanner inputs
        for i, line in enumerate(lines):
            m = re.search(r"\.next(Int|Double|Float|Boolean|Line|Byte|Short|Long|Char)\s*\(", line)
            if m:
                if i in skip_nextline_indexes:
                    continue
                dtype = m.group(1).lower()
                if dtype == "int":
                    types_found.append("int")
                elif dtype in ("double", "float"):
                    types_found.append("float")
                elif dtype == "boolean":
                    types_found.append("bool")
                elif dtype == "char":
                    types_found.append("char")
                else:
                    types_found.append("string")

        # Match args[] parsing without duplicates
        seen_args = set()
        for m in re.finditer(
            r"(Integer\.parseInt|Double\.parseDouble|Float\.parseFloat|Boolean\.parseBoolean)\s*\(\s*args\[(\d+)\]\s*\)",
            code
        ):
            method, idx = m.groups()
            if idx in seen_args:
                continue
            seen_args.add(idx)
            if method.startswith("Integer"):
                types_found.append("int")
            elif method.startswith(("Double", "Float")):
                types_found.append("float")
            elif method.startswith("Boolean"):
                types_found.append("bool")

        # Any remaining args[] without parsing → string
        for m in re.finditer(r"args\[(\d+)\]", code):
            idx = m.group(1)
            if idx not in seen_args:
                seen_args.add(idx)
                types_found.append("string")

    return types_found if types_found else ["string"]


def detect_input_count_from_code(code, lang="java"):
    return len(detect_input_types_from_code(code, lang))


def generate_edge_cases(input_type="int", count=10, num_inputs=1):
    """
    Generate edge cases for given input type(s) and number of variables.
    input_type can be a string (single type) or list (multiple types in order).
    """
    cases = []

    # Ensure input_type is always a list
    if isinstance(input_type, str):
        input_type = [input_type] * num_inputs
    elif isinstance(input_type, list):
        if len(input_type) < num_inputs:
            input_type += ["string"] * (num_inputs - len(input_type))

    print(f"\n[DEBUG] Generating test cases for: {input_type} ({num_inputs} inputs)")

    def gen_value(dtype):
        if dtype == "int":
            return random.randint(-10**6, 10**6)
        elif dtype == "float":
            return round(random.uniform(-1e6, 1e6), 4)
        elif dtype == "bool":
            return random.choice([True, False])
        elif dtype == "char":
            return chr(random.randint(65, 90))  # A-Z
        else:
            return "str" + str(random.randint(0, 9999))

    base_values = {
        "int": [0, 1, -1, 10**9, -(10**9)],
        "float": [0.0, 1.0, -1.0, 1e9, -1e9],
        "string": ["", "a", "abc", "x"*100, "1234"],
        "bool": [True, False],
        "char": ["a", "Z", "0", "#", " "]
    }

    # Base cases
    for _ in range(min(5, count)):
        case = []
        for dtype in input_type:
            case.append(random.choice(base_values.get(dtype, ["test"])))
        cases.append(" ".join(map(str, case)) + "\n")

    # Random cases
    for _ in range(count):
        case = []
        for dtype in input_type:
            case.append(gen_value(dtype))
        cases.append(" ".join(map(str, case)) + "\n")

    print(f"[DEBUG] Generated {len(cases)} test cases:")
    for idx, c in enumerate(cases, 1):
        preview = c.strip()
        if len(preview) > 60:
            preview = preview[:60] + "...(truncated)"
        print(f"  {idx}. {preview}")

    return cases


if __name__ == "__main__":
    for filename in os.listdir(INPUT_DIR):
        filepath = os.path.join(INPUT_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        # Detect language
        if filename.endswith(".java"):
            lang = "java"
        elif filename.endswith(".py"):
            lang = "python"
        else:
            print(f"[WARN] Skipping {filename}, unsupported file type.")
            continue

        detected_types = detect_input_types_from_code(code, lang)
        detected_inputs = detect_input_count_from_code(code, lang)

        print(f"\n[INFO] Processing '{filename}' → Types: {detected_types}, Inputs: {detected_inputs}")

        generate_edge_cases(input_type=detected_types, count=10, num_inputs=detected_inputs)
