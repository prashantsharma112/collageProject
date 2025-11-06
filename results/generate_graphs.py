# import os
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
#
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
#
# SUMMARY_FILE = os.path.join(RESULTS_DIR, "summary.json")
# PASS_FILE = os.path.join(RESULTS_DIR, "pass_stats.json")
#
# # Load data
# with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
#     summary = json.load(f)
#
# with open(PASS_FILE, "r", encoding="utf-8") as f:
#     pass_stats = json.load(f)
#
# df_summary = pd.DataFrame(summary)
# df_pass = pd.DataFrame(pass_stats)
#
# # ===================== 1. Accuracy (Pass Rate) =====================
# overall_pass = df_pass.groupby("model")["pass_rate"].mean().reset_index()
# overall_pass.plot(kind="bar", x="model", y="pass_rate", legend=False, color="skyblue")
# plt.title("Accuracy Comparison (Average Pass Rate)")
# plt.ylabel("Pass Rate (%)")
# plt.savefig(os.path.join(RESULTS_DIR, "accuracy_pass_rate.png"))
# plt.close()
#
# # ===================== 2. Performance (Execution Time) =====================
# time_cols = [c for c in df_summary.columns if c.endswith("_time")]
# df_summary[["file"] + time_cols].set_index("file").plot(kind="bar", figsize=(10,6))
# plt.title("Performance Comparison (Execution Time)")
# plt.ylabel("Time (seconds)")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig(os.path.join(RESULTS_DIR, "performance_time.png"))
# plt.close()
#
# # ===================== 3. BLEU Score Quality =====================
# bleu_cols = [c for c in df_summary.columns if c.endswith("_bleu")]
# df_summary[["file"] + bleu_cols].set_index("file").plot(kind="bar", figsize=(10,6))
# plt.title("BLEU Score Quality Comparison")
# plt.ylabel("BLEU Score")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig(os.path.join(RESULTS_DIR, "bleu_quality.png"))
# plt.close()
#
# # ===================== 4. Syntax Success/Failure =====================
# syntax_cols = [c for c in df_summary.columns if c.endswith("_syntax_ok")]
#
# # Convert True/False → 1/0 then take mean (% success)
# df_syntax = df_summary[syntax_cols].mean().reset_index()
# df_syntax.columns = ["model_syntax", "success_rate"]
# df_syntax["model"] = df_syntax["model_syntax"].str.replace("_syntax_ok", "")
# df_syntax["success_rate"] = df_syntax["success_rate"] * 100
#
# df_syntax.plot(kind="bar", x="model", y="success_rate", legend=False, color="lightgreen")
# plt.title("Syntax Success Rate Comparison")
# plt.ylabel("Success Rate (%)")
# plt.savefig(os.path.join(RESULTS_DIR, "syntax_success.png"))
# plt.close()
#
# print("[SAVED] All graphs created in results/ folder")
#



import os
import json
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

SUMMARY_FILE = os.path.join(RESULTS_DIR, "summary.json")
PASS_FILE = os.path.join(RESULTS_DIR, "pass_stats.json")

# Load data
with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
    summary = json.load(f)

with open(PASS_FILE, "r", encoding="utf-8") as f:
    pass_stats = json.load(f)

df_summary = pd.DataFrame(summary)
df_pass = pd.DataFrame(pass_stats)

# ======== Build Aggregated Table ========
# Accuracy
accuracy = df_pass.groupby("model")["pass_rate"].mean()

# Time
time_cols = [c for c in df_summary.columns if c.endswith("_time")]
time_avg = df_summary[time_cols].mean()
time_avg.index = time_avg.index.str.replace("_time", "")

# BLEU
bleu_cols = [c for c in df_summary.columns if c.endswith("_bleu")]
bleu_avg = df_summary[bleu_cols].mean()
bleu_avg.index = bleu_avg.index.str.replace("_bleu", "")

# Syntax
syntax_cols = [c for c in df_summary.columns if c.endswith("_syntax_ok")]
syntax_avg = df_summary[syntax_cols].mean() * 100
syntax_avg.index = syntax_avg.index.str.replace("_syntax_ok", "")

# Combine into one DataFrame
combined_df = pd.DataFrame({
    "Pass Rate (%)": accuracy,
    "Execution Time (s)": time_avg,
    "BLEU Score": bleu_avg,
    "Syntax Success (%)": syntax_avg
}).reset_index().rename(columns={"index": "Model"})

# Save table
combined_table_file = os.path.join(RESULTS_DIR, "combined_table.csv")
combined_df.to_csv(combined_table_file, index=False)

print("\n=== SUMMARY TABLE ===")
print(combined_df)
print(f"\n[SAVED] Table -> {combined_table_file}")

# ======== Plot Combined Graph ========
fig, ax1 = plt.subplots(figsize=(10,6))

# Bars = Pass rate & Syntax success
bar_width = 0.35
x = range(len(combined_df))

ax1.bar([i - bar_width/2 for i in x], combined_df["Pass Rate (%)"],
        width=bar_width, label="Pass Rate (%)", color="skyblue")
ax1.bar([i + bar_width/2 for i in x], combined_df["Syntax Success (%)"],
        width=bar_width, label="Syntax Success (%)", color="lightgreen")

ax1.set_ylabel("Accuracy / Syntax (%)")
ax1.set_xticks(x)
ax1.set_xticklabels(combined_df["Model"])
ax1.set_ylim(0, 110)

# Line plots for BLEU & Execution Time
ax2 = ax1.twinx()
ax2.plot(x, combined_df["BLEU Score"], marker="o", color="orange", label="BLEU Score")
ax2.plot(x, combined_df["Execution Time (s)"], marker="s", color="red", label="Execution Time (s)")
ax2.set_ylabel("BLEU / Time")

# Legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Model Comparison: Accuracy, Syntax, BLEU, and Time")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "combined_graph.png"))
plt.close()

print(f"[SAVED] Combined graph -> {os.path.join(RESULTS_DIR, 'combined_graph.png')}")
