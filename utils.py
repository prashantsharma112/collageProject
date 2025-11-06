import csv
import json
import os

# Ensure results folder exists
os.makedirs("results", exist_ok=True)

CSV_FILE = "results/scores.csv"
JSON_FILE = "results/summary.json"

def init_csv_log():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "sample_id", "model_name", "src_lang", "tgt_lang",
                "compilation_success", "unit_test_passed",
                "syntax_semantic_match", "BLEU_score", "CodeBLEU_score",
                "translation_time_ms"
            ])

def log_csv_entry(data):
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "sample_id", "model_name", "src_lang", "tgt_lang",
            "compilation_success", "unit_test_passed",
            "syntax_semantic_match", "BLEU_score", "CodeBLEU_score",
            "translation_time_ms"
        ])
        writer.writerow(data)

def log_json_entry(data):
    with open(JSON_FILE, mode="a") as f:
        json.dump(data, f)
        f.write("\n")
