import json
import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

# Find all pass_stats_* files
pass_files = [f for f in os.listdir(RESULTS_DIR) if f.startswith("pass_stats_") and f.endswith(".json")]

for pass_file in pass_files:
    # Extract model name (e.g., pass_stats_gemini.json → gemini)
    model_name = re.search(r"pass_stats_(.+)\.json", pass_file).group(1)

    metrics_file = os.path.join(RESULTS_DIR, f"evaluation_metrics_{model_name}.json")
    pass_stats_file = os.path.join(RESULTS_DIR, pass_file)
    merged_output_file = os.path.join(RESULTS_DIR, f"merged_results_{model_name}.json")

    if not os.path.exists(metrics_file):
        print(f"[SKIP] No metrics file for model '{model_name}'")
        continue

    with open(metrics_file, "r", encoding="utf-8") as f:
        metrics_data = json.load(f)

    with open(pass_stats_file, "r", encoding="utf-8") as f:
        pass_data = json.load(f)

    # Convert pass stats to dict for quick lookup
    pass_dict = {entry["file"]: entry for entry in pass_data}

    merged_data = []
    for metric in metrics_data:
        file_name = metric["file"]
        merged_entry = {**metric, **pass_dict.get(file_name, {}), "model": model_name}
        merged_data.append(merged_entry)

    with open(merged_output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

    print(f"[SAVED] Merged results for '{model_name}' saved to {merged_output_file}")
