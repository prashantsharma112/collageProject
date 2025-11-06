# import re
# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
#
# MODEL_NAME = "Salesforce/codet5p-770m"
# MAX_NEW_TOKENS = 64
#
# print(f"Loading model: {MODEL_NAME} ...")
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
#
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")
# model = model.to(device)
#
#
# def clean_java_code(java_code: str) -> str:
#     """
#     Removes all license headers, block comments, and single-line comments from Java code.
#     """
#     # Normalize line endings
#     java_code = java_code.replace("\r\n", "\n")
#
#     # Remove block comments (/* ... */) including license headers
#     java_code = re.sub(r"/\*[\s\S]*?\*/", "", java_code, flags=re.MULTILINE)
#
#     # Remove single-line comments (// ...)
#     java_code = re.sub(r"//.*", "", java_code)
#
#     # Remove extra spaces and empty lines
#     java_code = "\n".join(line.strip() for line in java_code.split("\n") if line.strip())
#
#     return java_code.strip()
#
#
# def summarize_java(java_code: str) -> str:
#     cleaned_code = clean_java_code(java_code)
#
#     # Debug output to verify cleaning
#     print("\n--- Cleaned Java Code ---\n")
#     print(cleaned_code)
#     print("\n--------------------------\n")
#
#     prompt = "summarize: " + java_code
#
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=MAX_NEW_TOKENS,
#         num_beams=5,
#         early_stopping=True
#     )
#     return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
#
#
# if __name__ == "__main__":
#     java_example = """
#     /*
#      * Licensed to the Apache Software Foundation (ASF) under one or more
#      * contributor license agreements.  See the NOTICE file distributed with
#      * this work for additional information regarding copyright ownership.
#      */
#     public class Hello {
#         public static void main(String[] args) {
#             System.out.println("Hello World");
#         }
#     }
#     """
#
#     print("=== Original Java Code ===")
#     print(java_example)
#
#     summary = summarize_java(java_example)
#     print("\n--- Generated NL Summary ---")
#     print(summary)

# def isPalindrome(input_str):
#     processed = input_str.replace(" ", "").lower()
#     return processed == processed[::-1]
#
# # Example usage
# if __name__ == "__main__":
#     text = input("Enter a string to check if it is a palindrome: ")
#     if isPalindrome(text):
#         print(f"✅ The string '{text}' is a palindrome.")
#     else:
#         print(f"❌ The string '{text}' is NOT a palindrome.")


# from transformers import AutoTokenizer, AutoModelForCausalLM
# print("🔹 Loading model…")
# model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-multi")
# tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-multi")
# print("✅ Model loaded successfully")
#
# import torch
#
# # PyTorch version
# print("PyTorch version:", torch.__version__)
#
# # CUDA availability
# print("CUDA available:", torch.cuda.is_available())
#
# # CUDA device info
# if torch.cuda.is_available():
#     print("CUDA device name:", torch.cuda.get_device_name(0))
#     print("CUDA version:", torch.version.cuda)
# else:
#     print("Using CPU")
#
#
#


import torch
print(torch.cuda.get_device_name(0))
print(f"Memory Allocated: {torch.cuda.memory_allocated()/1024**2:.2f} MB")
print(f"Memory Cached: {torch.cuda.memory_reserved()/1024**2:.2f} MB")
