#
#
# # count_pass_testcase.py
# import json
# import os
#
# # ===== CONFIG =====
# MODEL_NAME = "gemini"  # Change for each model
#
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# RESULTS_FILE = os.path.join(PROJECT_ROOT, f"translated_results_{MODEL_NAME}.json")
#
# # Ensure results directory exists
# RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
# os.makedirs(RESULTS_DIR, exist_ok=True)
#
# OUTPUT_FILE = os.path.join(RESULTS_DIR, f"pass_stats_{MODEL_NAME}.json")
# # ==================
#
# with open(RESULTS_FILE, "r", encoding="utf-8") as f:
#     data = json.load(f)
#
# pass_stats = []
#
# for prog_name, test_cases in data.items():
#     total = len(test_cases)
#     passed = sum(
#         1 for t in test_cases
#         if t["expected_output"].strip() == t["translated_output"].strip()
#            and t["expected_error"].strip() == t["translated_error"].strip()
#     )
#     pass_rate = round((passed / total * 100) if total > 0 else 0, 2)
#
#     pass_stats.append({
#         "model": MODEL_NAME,
#         "file": f"{prog_name}.java",  # or .py depending on source
#         "passed": passed,
#         "total": total,
#         "pass_rate": pass_rate
#     })
#
# with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     json.dump(pass_stats, f, indent=4, ensure_ascii=False)
#
# print(f"[SAVED] Pass stats for model '{MODEL_NAME}' saved to {OUTPUT_FILE}")



import json
import os

# ===== CONFIG =====
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

RESULTS_FILE = os.path.join(PROJECT_ROOT, "results", "translated_results.json")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "results", "pass_stats.json")
# ==================

if not os.path.exists(RESULTS_FILE):
    print("[ERROR] translated_results.json not found.")
    exit(1)

with open(RESULTS_FILE, "r", encoding="utf-8") as f:
    all_models_data = json.load(f)

pass_stats = []

for model_name, programs in all_models_data.items():
    for prog_name, test_cases in programs.items():
        total = len(test_cases)
        passed = sum(
            1 for t in test_cases
            if t["expected_output"].strip() == t["translated_output"].strip()
               and t["expected_error"].strip() == t["translated_error"].strip()
        )
        pass_rate = round((passed / total * 100) if total > 0 else 0, 2)

        pass_stats.append({
            "model": model_name,
            "file": f"{prog_name}.java",  # adjust if some are .py
            "passed": passed,
            "total": total,
            "pass_rate": pass_rate
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(pass_stats, f, indent=4, ensure_ascii=False)

print(f"[SAVED] Combined pass stats saved to {OUTPUT_FILE}")
