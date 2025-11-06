#
#
# #
#
# import os
# import json
# import time
# from evaluators.syntax_checker import check_syntax
# from dotenv import load_dotenv
# import sacrebleu
#
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper  # Your existing wrapper
# # from models.codet5_wrapper import Codet5Wrapper  # Optional if you also want Codet5
#
# # Initialize models
# gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
# # codegen_model = CodeGenWrapper(device="cpu")  # or "cpu" if no GPU
#
# # ==========================
# # Load previous results
# # ==========================
# summary_path = "results/summary.json"
# if os.path.exists(summary_path):
#     with open(summary_path, "r", encoding="utf-8") as f:
#         results = json.load(f)
# else:
#     results = []
#
# processed_files = {r["file"] for r in results}
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     while True:
#         try:
#             return model.translate(code, src_lang, tgt_lang)
#         except Exception as e:
#             print(f"❌ Error while translating: {e}")
#             return None
#
# # ==========================
# # Main Loop
# # ==========================
# for file in os.listdir(testcases_dir):
#     if file.endswith(".java") and file not in processed_files:
#         file_path = os.path.join(testcases_dir, file)
#         with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#             code = f.read()
#
#         # Gemini translation
#         gemini_translation = safe_translate(gemini_model, code, SRC_LANG, TGT_LANG)
#         # CodeGen translation
#         # codegen_translation = safe_translate(codegen_model, code, SRC_LANG, TGT_LANG)
#
#         # Save translations
#         gemini_file = os.path.join(output_dir, "gemini", file.replace(".java", ".py"))
#         os.makedirs(os.path.dirname(gemini_file), exist_ok=True)
#         with open(gemini_file, "w", encoding="utf-8") as out:
#             out.write(gemini_translation["code"])
#
#         # codegen_file = os.path.join(output_dir, "codegen", file.replace(".java", ".py"))
#         # os.makedirs(os.path.dirname(codegen_file), exist_ok=True)
#         # with open(codegen_file, "w", encoding="utf-8") as out:
#         #     out.write(codegen_translation["code"])
#
#         # Syntax check
#         gemini_syntax = check_syntax(gemini_translation["code"], lang=TGT_LANG)
#         # codegen_syntax = check_syntax(codegen_translation["code"], lang=TGT_LANG)
#
#         # Reference BLEU
#         reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#         if os.path.exists(reference_file):
#             with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                 reference_code = ref_f.read()
#             gemini_bleu = bleu_score(reference_code, gemini_translation["code"])
#             # codegen_bleu = bleu_score(reference_code, codegen_translation["code"])
#         else:
#             gemini_bleu = codegen_bleu = None
#
#         # Record results
#         results.append({
#             "file": file,
#             "gemini_translation_time": gemini_translation["time"],
#             # "codegen_translation_time": codegen_translation["time"],
#             "gemini_syntax_ok": gemini_syntax,
#             # "codegen_syntax_ok": codegen_syntax,
#             "gemini_bleu": gemini_bleu,
#             # "codegen_bleu": codegen_bleu
#         })
#
#         # Save summary
#         with open(summary_path, "w", encoding="utf-8") as out:
#             json.dump(results, out, indent=4, ensure_ascii=False)
#
# print(f"✅ Translation test completed. Summary saved to {summary_path}")
#


#
# import os
# import json
# import time
# from evaluators.syntax_checker import check_syntax
# from dotenv import load_dotenv
# import sacrebleu
#
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper
# from models.CodeT5Wrapper import CodeT5Wrapper
#
# # Initialize models
# gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
# codegen_model = CodeGenWrapper(device="cpu")       # or "cuda"
# codet5_model = CodeT5Wrapper(device="cpu")
#
# MODELS = {
#     "gemini": gemini_model,
#     "codegen": codegen_model,
#     "codet5": codet5_model,
# }
#
# # ==========================
# # Load previous results
# # ==========================
# summary_path = "results/summary.json"
# if os.path.exists(summary_path):
#     with open(summary_path, "r", encoding="utf-8") as f:
#         results = json.load(f)
# else:
#     results = []
#
# processed_files = {r["file"] for r in results}
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     if not reference or not hypothesis:
#         return None
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     start = time.time()
#     try:
#         result = model.translate(code, src_lang, tgt_lang)
#
#         if isinstance(result, dict) and "code" in result:
#             return {"code": result["code"], "time": result.get("time", round(time.time() - start, 2))}
#         elif isinstance(result, str):
#             return {"code": result, "time": round(time.time() - start, 2)}
#         else:
#             raise ValueError("Unexpected translation format")
#
#     except Exception as e:
#         print(f"❌ Error while translating with {model.__class__.__name__}: {e}")
#         return {"code": "", "time": None}
#
# # ==========================
# # Main Loop
# # ==========================
# for file in os.listdir(testcases_dir):
#     if file.endswith(".java") and file not in processed_files:
#         file_path = os.path.join(testcases_dir, file)
#         with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#             code = f.read()
#
#         # Run translations for all models
#         translations = {}
#         for name, model in MODELS.items():
#             translations[name] = safe_translate(model, code, SRC_LANG, TGT_LANG)
#
#         # Save outputs
#         for model_name, translation in translations.items():
#             if translation["code"]:
#                 out_file = os.path.join(output_dir, model_name, file.replace(".java", ".py"))
#                 os.makedirs(os.path.dirname(out_file), exist_ok=True)
#                 with open(out_file, "w", encoding="utf-8") as out:
#                     out.write(translation["code"])
#
#         # Syntax checks
#         syntax_results = {name: check_syntax(tr["code"], lang=TGT_LANG) for name, tr in translations.items()}
#
#         # Reference BLEU
#         reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#         if os.path.exists(reference_file):
#             with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                 reference_code = ref_f.read()
#             bleu_results = {name: bleu_score(reference_code, tr["code"]) for name, tr in translations.items()}
#         else:
#             bleu_results = {name: None for name in translations}
#
#         # Record results
#         entry = {"file": file}
#         for name, tr in translations.items():
#             entry[f"{name}_time"] = tr["time"]
#             entry[f"{name}_syntax_ok"] = syntax_results[name]
#             entry[f"{name}_bleu"] = bleu_results[name]
#         results.append(entry)
#
#         # Save summary incrementally
#         with open(summary_path, "w", encoding="utf-8") as out:
#             json.dump(results, out, indent=4, ensure_ascii=False)
#
# print(f"✅ Translation test completed. Summary saved to {summary_path}")
#





#
# import os
# import json
# import time
# from evaluators.syntax_checker import check_syntax
# from dotenv import load_dotenv
# import sacrebleu
# import subprocess
#
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper
#
# # Initialize models
# gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
# codegen_model = CodeGenWrapper(device="cpu")  # Change to "cuda" if GPU available
#
# # ==========================
# # Load previous results
# # ==========================
# summary_path = "results/summary.json"
# if os.path.exists(summary_path):
#     with open(summary_path, "r", encoding="utf-8") as f:
#         results = json.load(f)
# else:
#     results = []
#
# processed_files = {r["file"] for r in results}
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     try:
#         return model.translate(code, src_lang, tgt_lang)
#     except Exception as e:
#         print(f"❌ Error while translating: {e}")
#         return None
#
# # ==========================
# # Function to run test cases
# # ==========================
# def run_testcases(translated_file: str, test_count: int = 100):
#     """
#     Runs the external test case script with specified number of test cases.
#     """
#     try:
#         subprocess.run(
#             ["python", "run_sourceCode_testcase.py", translated_file, str(test_count)],
#             check=True
#         )
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Test case execution failed: {e}")
#         return False
#
# # ==========================
# # Main Loop
# # ==========================
# for file in os.listdir(testcases_dir):
#     if file.endswith(".java") and file not in processed_files:
#         file_path = os.path.join(testcases_dir, file)
#         with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#             code = f.read()
#
#         # Translate
#         gemini_translation = safe_translate(gemini_model, code, SRC_LANG, TGT_LANG)
#         codegen_translation = safe_translate(codegen_model, code, SRC_LANG, TGT_LANG)
#
#         if not gemini_translation or not codegen_translation:
#             continue
#
#         # Save translations
#         gemini_file = os.path.join(output_dir, "gemini", file.replace(".java", ".py"))
#         os.makedirs(os.path.dirname(gemini_file), exist_ok=True)
#         with open(gemini_file, "w", encoding="utf-8") as out:
#             out.write(gemini_translation["code"])
#
#         codegen_file = os.path.join(output_dir, "codegen", file.replace(".java", ".py"))
#         os.makedirs(os.path.dirname(codegen_file), exist_ok=True)
#         with open(codegen_file, "w", encoding="utf-8") as out:
#             out.write(codegen_translation["code"])
#
#         # Syntax check
#         gemini_syntax = check_syntax(gemini_translation["code"], lang=TGT_LANG)
#         codegen_syntax = check_syntax(codegen_translation["code"], lang=TGT_LANG)
#
#         # Test case execution results
#         gemini_tests_passed = None
#         codegen_tests_passed = None
#
#         if gemini_syntax:
#             gemini_tests_passed = run_testcases(gemini_file, 100)
#         else:
#             print("⚠ No test case executed for Gemini due to wrong syntax.")
#
#         if codegen_syntax:
#             codegen_tests_passed = run_testcases(codegen_file, 100)
#         else:
#             print("⚠ No test case executed for CodeGen due to wrong syntax.")
#
#         # BLEU score
#         reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#         if os.path.exists(reference_file):
#             with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                 reference_code = ref_f.read()
#             gemini_bleu = bleu_score(reference_code, gemini_translation["code"])
#             codegen_bleu = bleu_score(reference_code, codegen_translation["code"])
#         else:
#             gemini_bleu = codegen_bleu = None
#
#         # Record results
#         results.append({
#             "file": file,
#             "gemini_translation_time": gemini_translation["time"],
#             "codegen_translation_time": codegen_translation["time"],
#             "gemini_syntax_ok": gemini_syntax,
#             "codegen_syntax_ok": codegen_syntax,
#             "gemini_tests_passed": gemini_tests_passed,
#             "codegen_tests_passed": codegen_tests_passed,
#             "gemini_bleu": gemini_bleu,
#             "codegen_bleu": codegen_bleu
#         })
#
#         # Save summary
#         with open(summary_path, "w", encoding="utf-8") as out:
#             json.dump(results, out, indent=4, ensure_ascii=False)
#
# print(f"✅ Translation + Test case run completed. Summary saved to {summary_path}")


#
# import os
# import json
# import subprocess
# from dotenv import load_dotenv
# import sacrebleu
# from evaluators.syntax_checker import check_syntax
#
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# # Directories
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper
# # from models.PLBERTWrapper import PLBERTWrapper  # Uncomment if you add PLBERT
#
# # ==========================
# # Initialize models
# # ==========================
# models = {
#     "gemini": GeminiWrapper(api_key=GEMINI_API_KEY),
#     "codegen": CodeGenWrapper(device="cpu"),
#     # "plbert": PLBERTWrapper(device="cpu")  # Add later if needed
# }
#
# # ==========================
# # Load previous results
# # ==========================
# summary_path = "results/summary.json"
# if os.path.exists(summary_path):
#     with open(summary_path, "r", encoding="utf-8") as f:
#         results = json.load(f)
# else:
#     results = []
#
# processed_files = {r["file"] for r in results}
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     try:
#         return model.translate(code, src_lang, tgt_lang)
#     except Exception as e:
#         print(f"❌ Error while translating: {e}")
#         return None
#
# # ==========================
# # Function to run test cases
# # ==========================
# def run_testcases(translated_file: str, test_count: int = 100):
#     try:
#         subprocess.run(
#             ["python", "run_sourceCode_testcase.py", translated_file, str(test_count)],
#             check=True
#         )
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Test case execution failed: {e}")
#         return False
#
# # ==========================
# # Main Loop
# # ==========================
# for file in os.listdir(testcases_dir):
#     if file.endswith(".java") and file not in processed_files:
#         file_path = os.path.join(testcases_dir, file)
#         with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#             code = f.read()
#
#         file_results = {"file": file}
#
#         for model_name, model in models.items():
#             print(f"\n🚀 Translating {file} using {model_name}...")
#             translation = safe_translate(model, code, SRC_LANG, TGT_LANG)
#             if not translation:
#                 file_results[f"{model_name}_syntax_ok"] = False
#                 file_results[f"{model_name}_tests_passed"] = None
#                 file_results[f"{model_name}_bleu"] = None
#                 continue
#
#             # Save translation
#             model_dir = os.path.join(output_dir, model_name)
#             os.makedirs(model_dir, exist_ok=True)
#             output_file = os.path.join(model_dir, file.replace(".java", ".py"))
#             with open(output_file, "w", encoding="utf-8") as out:
#                 out.write(translation["code"])
#
#             # Syntax check
#             syntax_ok = check_syntax(translation["code"], lang=TGT_LANG)
#             file_results[f"{model_name}_syntax_ok"] = syntax_ok
#
#             # Run test cases if syntax is okay
#             if syntax_ok:
#                 tests_passed = run_testcases(output_file, 100)
#                 file_results[f"{model_name}_tests_passed"] = tests_passed
#             else:
#                 print(f"⚠ Skipping tests for {model_name} due to syntax error.")
#                 file_results[f"{model_name}_tests_passed"] = None
#
#             # BLEU score
#             reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#             if os.path.exists(reference_file):
#                 with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                     reference_code = ref_f.read()
#                 bleu = bleu_score(reference_code, translation["code"])
#             else:
#                 bleu = None
#             file_results[f"{model_name}_bleu"] = bleu
#
#             # Save translation time if available
#             if "time" in translation:
#                 file_results[f"{model_name}_translation_time"] = translation["time"]
#
#         results.append(file_results)
#
#         with open(summary_path, "w", encoding="utf-8") as out:
#             json.dump(results, out, indent=4, ensure_ascii=False)
#
# print(f"✅ Translation + Test case run completed. Summary saved to {summary_path}")
#
#
#
# import os
# import json
# import subprocess
# from dotenv import load_dotenv
# import sacrebleu
# from evaluators.syntax_checker import check_syntax
#
#
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# # Directories
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# # from models.CodeGenWrapper import CodeGenWrapper
# # from models.PLBERTWrapper import PLBERTWrapper  # Uncomment if you add PLBERT
#
# # ==========================
# # Initialize models
# # ==========================
# models = {
#     "gemini": GeminiWrapper(api_key=GEMINI_API_KEY),
#     # "codegen": CodeGenWrapper(device="cpu"),
#     # "plbert": PLBERTWrapper(device="cpu")  # Add later if needed
# }
#
# # ==========================
# # Load previous results
# # ==========================
# summary_path = "results/summary.json"
# testcase_results_path = "results/testcase_results.json"
#
# if os.path.exists(summary_path):
#     with open(summary_path, "r", encoding="utf-8") as f:
#         results = json.load(f)
# else:
#     results = []
#
# if os.path.exists(testcase_results_path):
#     with open(testcase_results_path, "r", encoding="utf-8") as f:
#         testcase_results = json.load(f)
# else:
#     testcase_results = []
#
# processed_files = {r["file"] for r in results}
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     try:
#         return model.translate(code, src_lang, tgt_lang)
#     except Exception as e:
#         print(f"❌ Error while translating: {e}")
#         return None
#
# # ==========================
# # Function to run test cases (returns detailed results)
# # ==========================
# def run_testcases(translated_file: str, test_count: int = 100):
#     try:
#         proc = subprocess.run(
#             ["python", "evaluators/run_sourceCode_testcase.py", translated_file, str(test_count)],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#
#         try:
#             # Parse JSON output if run_sourceCode_testcase.py returns structured data
#             return json.loads(proc.stdout)
#         except json.JSONDecodeError:
#             # Fallback: return raw text
#             return {"raw_output": proc.stdout.strip(), "error_output": proc.stderr.strip()}
#
#     except subprocess.CalledProcessError as e:
#         return {"error": f"Test case execution failed: {e.stderr}"}
#
# # ==========================
# # Main Loop
# # ==========================
# for file in os.listdir(testcases_dir):
#     if file.endswith(".java") and file not in processed_files:
#         file_path = os.path.join(testcases_dir, file)
#         with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#             code = f.read()
#
#         file_results = {"file": file}
#         file_testcase_results = {"file": file, "models": {}}
#
#         for model_name, model in models.items():
#             print(f"\n🚀 Translating {file} using {model_name}...")
#             translation = safe_translate(model, code, SRC_LANG, TGT_LANG)
#             if not translation:
#                 file_results[f"{model_name}_syntax_ok"] = False
#                 file_results[f"{model_name}_tests_passed"] = None
#                 file_results[f"{model_name}_bleu"] = None
#                 file_testcase_results["models"][model_name] = None
#                 continue
#
#             # Save translation
#             model_dir = os.path.join(output_dir, model_name)
#             os.makedirs(model_dir, exist_ok=True)
#             output_file = os.path.join(model_dir, file.replace(".java", ".py"))
#             with open(output_file, "w", encoding="utf-8") as out:
#                 out.write(translation["code"])
#
#             # Syntax check
#             syntax_ok = check_syntax(translation["code"], lang=TGT_LANG)
#             file_results[f"{model_name}_syntax_ok"] = syntax_ok
#
#             # Run test cases if syntax is okay
#             if syntax_ok:
#                 tc_result = run_testcases(output_file, 100)
#                 file_testcase_results["models"][model_name] = tc_result
#
#                 # Mark pass/fail for summary
#                 file_results[f"{model_name}_tests_passed"] = not bool(tc_result.get("error"))
#             else:
#                 print(f"⚠ Skipping tests for {model_name} due to syntax error.")
#                 file_results[f"{model_name}_tests_passed"] = None
#                 file_testcase_results["models"][model_name] = None
#
#             # BLEU score
#             reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#             if os.path.exists(reference_file):
#                 with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                     reference_code = ref_f.read()
#                 bleu = bleu_score(reference_code, translation["code"])
#             else:
#                 bleu = None
#             file_results[f"{model_name}_bleu"] = bleu
#
#             # Save translation time if available
#             if "time" in translation:
#                 file_results[f"{model_name}_translation_time"] = translation["time"]
#
#         results.append(file_results)
#         testcase_results.append(file_testcase_results)
#
#         # Save both files
#         with open(summary_path, "w", encoding="utf-8") as out:
#             json.dump(results, out, indent=4, ensure_ascii=False)
#
#         with open(testcase_results_path, "w", encoding="utf-8") as out:
#             json.dump(testcase_results, out, indent=4, ensure_ascii=False)
#
# print(f"✅ Translation + Test case run completed.")
# print(f"📄 Summary saved to {summary_path}")
# print(f"📄 Detailed test case results saved to {testcase_results_path}")
#


# working
# import os
# import sys
# import time
# import json
# import subprocess
# from dotenv import load_dotenv
# import sacrebleu
#
#
# # ✅ Ensure local imports work no matter where you run from
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper
# from models.CodeT5Wrapper import CodeT5Wrapper
# from evaluators.syntax_checker import check_syntax
#
#
# # Initialize models
# gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
# codegen_model = CodeGenWrapper(device="cpu")       # change to "cuda" if GPU available
# codet5_model = CodeT5Wrapper(device="cpu")
#
# MODELS = {
#     "gemini": gemini_model,
#     "codegen": codegen_model,
#     "codet5": codet5_model,
# }
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     if not reference or not hypothesis:
#         return None
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     start = time.time()
#     try:
#         result = model.translate(code, src_lang, tgt_lang)
#
#         if isinstance(result, dict) and "code" in result:
#             return {"code": result["code"], "time": result.get("time", round(time.time() - start, 2))}
#         elif isinstance(result, str):
#             return {"code": result, "time": round(time.time() - start, 2)}
#         else:
#             raise ValueError("Unexpected translation format")
#
#     except Exception as e:
#         print(f"❌ Error while translating with {model.__class__.__name__}: {e}")
#         return {"code": "", "time": None}
#
# # ==========================
# # Step Runner
# # ==========================
# def run_step(script, args=None):
#     cmd = ["python", script]
#     if args:
#         cmd += args
#     print(f"\n=== Running {script} {' '.join(args or [])} ===")
#     result = subprocess.run(cmd)
#     if result.returncode != 0:
#         print(f"❌ Error in {script}")
#         sys.exit(1)
#
# # ==========================
# # Main Pipeline
# # ==========================
# if __name__ == "__main__":
#     BASE = os.path.dirname(os.path.abspath(__file__))
#     EVAL = os.path.join(BASE, "evaluators")
#     # 1. Run original source programs with testcases
#     run_step(os.path.join(EVAL, "run_sourceCode_testcase.py"))
#
#     # 2. Translation + BLEU + Syntax
#     summary_path = "results/summary.json"
#     if os.path.exists(summary_path):
#         with open(summary_path, "r", encoding="utf-8") as f:
#             results = json.load(f)
#     else:
#         results = []
#
#     processed_files = {r["file"] for r in results}
#
#     for file in os.listdir(testcases_dir):
#         if file.endswith(".java") and file not in processed_files:
#             file_path = os.path.join(testcases_dir, file)
#             with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#                 code = f.read()
#
#             # Run translations for all models
#             translations = {}
#             for name, model in MODELS.items():
#                 translations[name] = safe_translate(model, code, SRC_LANG, TGT_LANG)
#
#             # Save outputs
#             for model_name, translation in translations.items():
#                 if translation["code"]:
#                     out_file = os.path.join(output_dir, model_name, file.replace(".java", ".py"))
#                     os.makedirs(os.path.dirname(out_file), exist_ok=True)
#                     with open(out_file, "w", encoding="utf-8") as out:
#                         out.write(translation["code"])
#
#             # Syntax checks
#             syntax_results = {name: check_syntax(tr["code"], lang=TGT_LANG) for name, tr in translations.items()}
#
#             # Reference BLEU
#             reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#             if os.path.exists(reference_file):
#                 with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                     reference_code = ref_f.read()
#                 bleu_results = {name: bleu_score(reference_code, tr["code"]) for name, tr in translations.items()}
#             else:
#                 bleu_results = {name: None for name in translations}
#
#             # Record results
#             entry = {"file": file}
#             for name, tr in translations.items():
#                 entry[f"{name}_time"] = tr["time"]
#                 entry[f"{name}_syntax_ok"] = syntax_results[name]
#                 entry[f"{name}_bleu"] = bleu_results[name]
#             results.append(entry)
#
#             # Save summary incrementally
#             with open(summary_path, "w", encoding="utf-8") as out:
#                 json.dump(results, out, indent=4, ensure_ascii=False)
#
#     print(f"\n✅ Translation completed. Summary saved to {summary_path}")
#
#     # 3. Run translated programs with same testcases
#     run_step(os.path.join(EVAL, "run_translateCode_testcase.py"))
#
#     # 4. Count pass/fail testcases for each model
#     for model in ["gemini", "codegen", "codet5"]:
#         run_step(os.path.join(EVAL, "count_pass_testcase.py"), args=[model])
#
#     print("\n🎉 Full pipeline completed successfully!")
#





#
# import os
# import sys
# import time
# import json
# import subprocess
# from dotenv import load_dotenv
# import sacrebleu
#
#
# # ✅ Ensure local imports work no matter where you run from
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper
# from models.CodeT5Wrapper import CodeT5Wrapper
# from models.HybridWrapper import HybridWrapper
# from evaluators.syntax_checker import check_syntax
#
#
# # Initialize models
# gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
# codegen_model = CodeGenWrapper(device="cpu")       # change to "cuda" if GPU available
# codet5_model = CodeT5Wrapper(device="cpu")
# hybrid_model = HybridWrapper(device="cpu")
#
# MODELS = {
#     "gemini": gemini_model,
#     "codegen": codegen_model,
#     "codet5": codet5_model,
#     "hybrid": hybrid_model,
# }
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     if not reference or not hypothesis:
#         return None
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     start = time.time()
#     try:
#         result = model.translate(code, src_lang, tgt_lang)
#
#         if isinstance(result, dict) and "code" in result:
#             return {"code": result["code"], "time": result.get("time", round(time.time() - start, 2))}
#         elif isinstance(result, str):
#             return {"code": result, "time": round(time.time() - start, 2)}
#         else:
#             raise ValueError("Unexpected translation format")
#
#     except Exception as e:
#         print(f"❌ Error while translating with {model.__class__.__name__}: {e}")
#         return {"code": "", "time": None}
#
# # ==========================
# # Step Runner
# # ==========================
# def run_step(script, args=None):
#     cmd = ["python", script]
#     if args:
#         cmd += args
#     print(f"\n=== Running {script} {' '.join(args or [])} ===")
#     result = subprocess.run(cmd)
#     if result.returncode != 0:
#         print(f"❌ Error in {script}")
#         sys.exit(1)
#
# # ==========================
# # Main Pipeline
# # ==========================
# if __name__ == "__main__":
#     BASE = os.path.dirname(os.path.abspath(__file__))
#     EVAL = os.path.join(BASE, "evaluators")
#     # 1. Run original source programs with testcases
#     run_step(os.path.join(EVAL, "run_sourceCode_testcase.py"))
#
#     # 2. Translation + BLEU + Syntax
#     summary_path = "results/summary.json"
#     if os.path.exists(summary_path):
#         with open(summary_path, "r", encoding="utf-8") as f:
#             results = json.load(f)
#     else:
#         results = []
#
#     processed_files = {r["file"] for r in results}
#
#     for file in os.listdir(testcases_dir):
#         if file.endswith(".java") and file not in processed_files:
#             file_path = os.path.join(testcases_dir, file)
#             with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#                 code = f.read()
#
#             # Run translations for all models
#             translations = {}
#             for name, model in MODELS.items():
#                 translations[name] = safe_translate(model, code, SRC_LANG, TGT_LANG)
#
#             # Save outputs
#             for model_name, translation in translations.items():
#                 if translation["code"]:
#                     out_file = os.path.join(output_dir, model_name, file.replace(".java", ".py"))
#                     os.makedirs(os.path.dirname(out_file), exist_ok=True)
#                     with open(out_file, "w", encoding="utf-8") as out:
#                         out.write(translation["code"])
#
#             # Syntax checks
#             syntax_results = {name: check_syntax(tr["code"], lang=TGT_LANG) for name, tr in translations.items()}
#
#             # Reference BLEU
#             reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#             if os.path.exists(reference_file):
#                 with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                     reference_code = ref_f.read()
#                 bleu_results = {name: bleu_score(reference_code, tr["code"]) for name, tr in translations.items()}
#             else:
#                 bleu_results = {name: None for name in translations}
#
#             # Record results
#             entry = {"file": file}
#             for name, tr in translations.items():
#                 entry[f"{name}_time"] = tr["time"]
#                 entry[f"{name}_syntax_ok"] = syntax_results[name]
#                 entry[f"{name}_bleu"] = bleu_results[name]
#             results.append(entry)
#
#             # Save summary incrementally
#             with open(summary_path, "w", encoding="utf-8") as out:
#                 json.dump(results, out, indent=4, ensure_ascii=False)
#
#     print(f"\n✅ Translation completed. Summary saved to {summary_path}")
#
#     # 3. Run translated programs with same testcases
#     run_step(os.path.join(EVAL, "run_translateCode_testcase.py"))
#
#     # 4. Count pass/fail testcases for each model
#     for model in ["gemini", "codegen", "codet5", "hybrid"]:
#         run_step(os.path.join(EVAL, "count_pass_testcase.py"), args=[model])
#
#     print("\n🎉 Full pipeline completed successfully!")







#
#
#
# import os
# import sys
# import time
# import json
# import subprocess
# from dotenv import load_dotenv
# import sacrebleu
# import torch
#
# # ✅ Ensure local imports work no matter where you run from
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# # ==========================
# # Load environment variables
# # ==========================
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # ==========================
# # Import wrappers
# # ==========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper
# from models.CodeT5Wrapper import CodeT5Wrapper
# from models.HybridWrapper import HybridWrapper   # updated: use proper wrapper class
# from evaluators.syntax_checker import check_syntax
#
# # ==========================
# # Initialize models
# # ==========================
# gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
# codegen_model = CodeGenWrapper(device="cpu")       # change to "cuda" if GPU available
# codet5_model = CodeT5Wrapper(device="cpu")
# hybrid_model = HybridWrapper(device="cpu")        # Hybrid wrapper now takes input from main script
#
# MODELS = {
#     "gemini": gemini_model,
#     "codegen": codegen_model,
#     "codet5": codet5_model,
#     "hybrid": hybrid_model,
# }
#
# # ==========================
# # BLEU Score
# # ==========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     if not reference or not hypothesis:
#         return None
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # ==========================
# # Safe translate wrapper
# # ==========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     start = time.time()
#     try:
#         result = model.translate(code, src_lang, tgt_lang)
#
#         if isinstance(result, dict) and "code" in result:
#             return {"code": result["code"], "time": result.get("time", round(time.time() - start, 2))}
#         elif isinstance(result, str):
#             return {"code": result, "time": round(time.time() - start, 2)}
#         else:
#             raise ValueError("Unexpected translation format")
#
#     except Exception as e:
#         print(f"❌ Error while translating with {model.__class__.__name__}: {e}")
#         return {"code": "", "time": None}
#
# # ==========================
# # Step Runner
# # ==========================
# def run_step(script, args=None):
#     cmd = ["python", script]
#     if args:
#         cmd += args
#     print(f"\n=== Running {script} {' '.join(args or [])} ===")
#     result = subprocess.run(cmd)
#     if result.returncode != 0:
#         print(f"❌ Error in {script}")
#         sys.exit(1)
#
# # ==========================
# # Main Pipeline
# # ==========================
# if __name__ == "__main__":
#     BASE = os.path.dirname(os.path.abspath(__file__))
#     EVAL = os.path.join(BASE, "evaluators")
#
#     # 1. Run original source programs with testcases
#     run_step(os.path.join(EVAL, "run_sourceCode_testcase.py"))
#
#     # 2. Translation + BLEU + Syntax
#     summary_path = "results/summary.json"
#     if os.path.exists(summary_path):
#         with open(summary_path, "r", encoding="utf-8") as f:
#             results = json.load(f)
#     else:
#         results = []
#
#     processed_files = {r["file"] for r in results}
#
#     for file in os.listdir(testcases_dir):
#         if file.endswith(".java") and file not in processed_files:
#             file_path = os.path.join(testcases_dir, file)
#             with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#                 code = f.read()
#
#             # Run translations for all models
#             translations = {}
#             for name, model in MODELS.items():
#                 translations[name] = safe_translate(model, code, SRC_LANG, TGT_LANG)  # input from main script
#
#             # Save outputs
#             for model_name, translation in translations.items():
#                 if translation["code"]:
#                     out_file = os.path.join(output_dir, model_name, file.replace(".java", ".py"))
#                     os.makedirs(os.path.dirname(out_file), exist_ok=True)
#                     with open(out_file, "w", encoding="utf-8") as out:
#                         out.write(translation["code"])
#
#             # Syntax checks
#             syntax_results = {name: check_syntax(tr["code"], lang=TGT_LANG) for name, tr in translations.items()}
#
#             # Reference BLEU
#             reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#             if os.path.exists(reference_file):
#                 with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                     reference_code = ref_f.read()
#                 bleu_results = {name: bleu_score(reference_code, tr["code"]) for name, tr in translations.items()}
#             else:
#                 bleu_results = {name: None for name in translations}
#
#             # Record results
#             entry = {"file": file}
#             for name, tr in translations.items():
#                 entry[f"{name}_time"] = tr["time"]
#                 entry[f"{name}_syntax_ok"] = syntax_results[name]
#                 entry[f"{name}_bleu"] = bleu_results[name]
#             results.append(entry)
#
#             # Save summary incrementally
#             with open(summary_path, "w", encoding="utf-8") as out:
#                 json.dump(results, out, indent=4, ensure_ascii=False)
#
#     print(f"\n✅ Translation completed. Summary saved to {summary_path}")
#
#     # 3. Run translated programs with same testcases
#     run_step(os.path.join(EVAL, "run_translateCode_testcase.py"))
#
#     # 4. Count pass/fail testcases for each model
#     for model in list(MODELS.keys()):
#         run_step(os.path.join(EVAL, "count_pass_testcase.py"), args=[model])
#
#     print("\n🎉 Full pipeline completed successfully!")



#
#
# import os
# import sys
# import time
# import json
# import subprocess
# from dotenv import load_dotenv
# import sacrebleu
#
# # =========================
# # Environment setup
# # =========================
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")
#
# SRC_LANG = "java"
# TGT_LANG = "python"
#
# testcases_dir = "input_program/"
# reference_dir = "references/"
# output_dir = "translated/"
# os.makedirs(output_dir, exist_ok=True)
# os.makedirs("results", exist_ok=True)
#
# # =========================
# # Import wrappers
# # =========================
# from models.GeminiWrapper import GeminiWrapper
# from models.CodeGenWrapper import CodeGenWrapper
# from models.CodeT5Wrapper import CodeT5Wrapper
# from models.HybridWrapper import HybridWrapper
# from evaluators.syntax_checker import check_syntax
#
# # =========================
# # Initialize models
# # =========================
# print("🔹 Initializing models...")
# gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
# codegen_model = CodeGenWrapper(device="cpu")       # change to "cuda" if GPU available
# codet5_model = CodeT5Wrapper(device="cpu")
# hybrid_model = HybridWrapper(device="cpu")        # Lazy load safe
# MODELS = {
#     "gemini": gemini_model,
#     "codegen": codegen_model,
#     "codet5": codet5_model,
#     "hybrid": hybrid_model,
# }
#
# # =========================
# # BLEU score
# # =========================
# def bleu_score(reference: str, hypothesis: str) -> float:
#     if not reference or not hypothesis:
#         return None
#     return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score
#
# # =========================
# # Safe translate wrapper
# # =========================
# def safe_translate(model, code, src_lang, tgt_lang):
#     start = time.time()
#     try:
#         result = model.translate(code, src_lang, tgt_lang)
#         if isinstance(result, dict) and "code" in result:
#             return {"code": result["code"], "time": result.get("time", round(time.time() - start, 2))}
#         elif isinstance(result, str):
#             return {"code": result, "time": round(time.time() - start, 2)}
#         else:
#             raise ValueError("Unexpected translation format")
#     except Exception as e:
#         print(f"❌ Error while translating with {model.__class__.__name__}: {e}")
#         return {"code": "", "time": None}
#
# # =========================
# # Run step
# # =========================
# def run_step(script, args=None):
#     cmd = ["python", script]
#     if args:
#         cmd += args
#     print(f"\n=== Running {script} {' '.join(args or [])} ===")
#     result = subprocess.run(cmd)
#     if result.returncode != 0:
#         print(f"❌ Error in {script}")
#         sys.exit(1)
#
# # =========================
# # Main pipeline
# # =========================
# if __name__ == "__main__":
#     BASE = os.path.dirname(os.path.abspath(__file__))
#     EVAL = os.path.join(BASE, "evaluators")
#
#     # 1. Run original source programs
#     run_step(os.path.join(EVAL, "run_sourceCode_testcase.py"))
#
#     # 2. Translation + BLEU + Syntax
#     summary_path = "results/summary.json"
#     results = json.load(open(summary_path, "r", encoding="utf-8")) if os.path.exists(summary_path) else []
#     processed_files = {r["file"] for r in results}
#
#     for file in os.listdir(testcases_dir):
#         if file.endswith(".java") and file not in processed_files:
#             file_path = os.path.join(testcases_dir, file)
#             with open(file_path, "r", encoding="utf-8", errors="replace") as f:
#                 code = f.read()
#
#             translations = {name: safe_translate(model, code, SRC_LANG, TGT_LANG) for name, model in MODELS.items()}
#
#             # Save outputs
#             for model_name, translation in translations.items():
#                 if translation["code"]:
#                     out_file = os.path.join(output_dir, model_name, file.replace(".java", ".py"))
#                     os.makedirs(os.path.dirname(out_file), exist_ok=True)
#                     with open(out_file, "w", encoding="utf-8") as out:
#                         out.write(translation["code"])
#
#             # Syntax checks
#             syntax_results = {name: check_syntax(tr["code"], lang=TGT_LANG) for name, tr in translations.items()}
#
#             # Reference BLEU
#             reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
#             if os.path.exists(reference_file):
#                 with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
#                     reference_code = ref_f.read()
#                 bleu_results = {name: bleu_score(reference_code, tr["code"]) for name, tr in translations.items()}
#             else:
#                 bleu_results = {name: None for name in translations}
#
#             # Record results
#             entry = {"file": file}
#             for name, tr in translations.items():
#                 entry[f"{name}_time"] = tr["time"]
#                 entry[f"{name}_syntax_ok"] = syntax_results[name]
#                 entry[f"{name}_bleu"] = bleu_results[name]
#             results.append(entry)
#
#             # Save summary incrementally
#             with open(summary_path, "w", encoding="utf-8") as out:
#                 json.dump(results, out, indent=4, ensure_ascii=False)
#
#     print(f"\n✅ Translation completed. Summary saved to {summary_path}")
#
#     # 3. Run translated programs
#     run_step(os.path.join(EVAL, "run_translateCode_testcase.py"))
#
#     # 4. Count pass/fail
#     for model in MODELS.keys():
#         run_step(os.path.join(EVAL, "count_pass_testcase.py"), args=[model])
#
#     print("\n🎉 Full pipeline completed successfully!")










import os
import sys
import time
import json
import subprocess
import re
import sacrebleu
from dotenv import load_dotenv

# =========================
# Environment setup
# =========================
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Please set it as an environment variable.")

SRC_LANG = "java"
TGT_LANG = "python"

testcases_dir = "input_program/"
reference_dir = "references/"
output_dir = "translated/"
os.makedirs(output_dir, exist_ok=True)
os.makedirs("results", exist_ok=True)

# =========================
# Code cleaner
# =========================
def extract_python_code(text: str) -> str:
    """
    Extracts and cleans only valid Python code from model outputs.
    Removes Java remnants, prompt text, and duplicates.
    """
    if not text:
        return ""

    # 1️⃣ Extract code from markdown fences if present
    blocks = re.findall(r"```(?:python)?(.*?)```", text, re.DOTALL)
    if blocks:
        text = "\n\n".join(blocks).strip()

    # 2️⃣ Remove lines that are obviously Java or prompt junk
    cleaned_lines = []
    for line in text.splitlines():
        if any(
            junk in line
            for junk in [
                "Translate the following",
                "Here’s a brief",
                "public static",
                "System.out",
                "Scanner ",
                "import java",
                "class ",
                "}", "{"
            ]
        ):
            continue
        if line.strip().startswith(("/*", "//", "# +", "# -", "#!", "# ")):
            continue
        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines).strip()

    # 3️⃣ Trim leading non-code explanations if any
    match = re.search(r"(import\s+\w+|def\s+\w+\s*\(|class\s+\w+\s*:|if\s+__name__)", cleaned_text)
    if match:
        cleaned_text = cleaned_text[match.start():]

    return cleaned_text.strip()

# =========================
# Import wrappers
# =========================
from models.GeminiWrapper import GeminiWrapper
from models.CodeGenWrapper import CodeGenWrapper
from models.CodeT5Wrapper import CodeT5Wrapper
from models.HybridWrapper import HybridWrapper
from evaluators.syntax_checker import check_syntax

# =========================
# Initialize models
# =========================
print("🔹 Initializing models...")
gemini_model = GeminiWrapper(api_key=GEMINI_API_KEY)
codegen_model = CodeGenWrapper(device="cpu")
codet5_model = CodeT5Wrapper(device="cpu")
hybrid_model = HybridWrapper(device="cpu")

MODELS = {
    "gemini": gemini_model,
    "codegen": codegen_model,
    "codet5": codet5_model,
    "hybrid": hybrid_model,
}

# =========================
# BLEU score function
# =========================
def bleu_score(reference: str, hypothesis: str) -> float:
    if not reference or not hypothesis:
        return None
    return sacrebleu.corpus_bleu([hypothesis], [[reference]]).score

# =========================
# Safe translate wrapper
# =========================
def safe_translate(model, code, src_lang, tgt_lang):
    start = time.time()
    try:
        result = model.translate(code, src_lang, tgt_lang)
        if isinstance(result, dict) and "code" in result:
            return {"code": result["code"], "time": result.get("time", round(time.time() - start, 2))}
        elif isinstance(result, str):
            return {"code": result, "time": round(time.time() - start, 2)}
        else:
            raise ValueError("Unexpected translation format")
    except Exception as e:
        print(f"❌ Error while translating with {model.__class__.__name__}: {e}")
        return {"code": "", "time": None}

# =========================
# Run step (for eval scripts)
# =========================
def run_step(script, args=None):
    cmd = ["python", script]
    if args:
        cmd += args
    print(f"\n=== Running {script} {' '.join(args or [])} ===")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ Error in {script}")
        sys.exit(1)

# =========================
# Main pipeline
# =========================
if __name__ == "__main__":
    BASE = os.path.dirname(os.path.abspath(__file__))
    EVAL = os.path.join(BASE, "evaluators")

    # 1️⃣ Run source Java programs
    run_step(os.path.join(EVAL, "run_sourceCode_testcase.py"))

    # 2️⃣ Translation + BLEU + Syntax
    summary_path = "results/summary.json"
    results = json.load(open(summary_path, "r", encoding="utf-8")) if os.path.exists(summary_path) else []
    processed_files = {r["file"] for r in results}

    for file in os.listdir(testcases_dir):
        if file.endswith(".java") and file not in processed_files:
            file_path = os.path.join(testcases_dir, file)
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                code = f.read()

            translations = {}
            for name, model in MODELS.items():
                result = safe_translate(model, code, SRC_LANG, TGT_LANG)
                cleaned_code = extract_python_code(result["code"])
                result["code"] = cleaned_code
                translations[name] = result

            # Save outputs
            for model_name, translation in translations.items():
                if translation["code"]:
                    out_file = os.path.join(output_dir, model_name, file.replace(".java", ".py"))
                    os.makedirs(os.path.dirname(out_file), exist_ok=True)
                    with open(out_file, "w", encoding="utf-8") as out:
                        out.write(translation["code"])

            # Syntax checks
            syntax_results = {name: check_syntax(tr["code"], lang=TGT_LANG) for name, tr in translations.items()}

            # Reference BLEU
            reference_file = os.path.join(reference_dir, file.replace(".java", ".py"))
            if os.path.exists(reference_file):
                with open(reference_file, "r", encoding="utf-8", errors="replace") as ref_f:
                    reference_code = ref_f.read()
                bleu_results = {name: bleu_score(reference_code, tr["code"]) for name, tr in translations.items()}
            else:
                bleu_results = {name: None for name in translations}

            # Record results
            entry = {"file": file}
            for name, tr in translations.items():
                entry[f"{name}_time"] = tr["time"]
                entry[f"{name}_syntax_ok"] = syntax_results[name]
                entry[f"{name}_bleu"] = bleu_results[name]
            results.append(entry)

            # Save summary incrementally
            with open(summary_path, "w", encoding="utf-8") as out:
                json.dump(results, out, indent=4, ensure_ascii=False)

    print(f"\n✅ Translation completed. Summary saved to {summary_path}")

    # 3️⃣ Run translated programs
    run_step(os.path.join(EVAL, "run_translateCode_testcase.py"))

    # 4️⃣ Count pass/fail per model
    for model in MODELS.keys():
        run_step(os.path.join(EVAL, "count_pass_testcase.py"), args=[model])

    print("\n🎉 Full pipeline completed successfully!")
