# import time
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
#
#
# class CodeGenWrapper:
#     def __init__(self, model_name="Salesforce/codegen-350M-multi", device=None):
#         """
#         Initialize CodeGen model and tokenizer.
#         """
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(model_name)
#
#         # Set padding token
#         if self.tokenizer.pad_token is None:
#             self.tokenizer.pad_token = self.tokenizer.eos_token
#
#         # Device setup
#         self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self.model.to(self.device)
#
#     def translate(self, code, src_lang="java", tgt_lang="python", max_new_tokens=256):
#         """
#         Translate code from src_lang to tgt_lang using CodeGen.
#         Returns translated code and elapsed time.
#         """
#         prompt = f"""\"\"\"Translate the following {src_lang} code to {tgt_lang}:
#
# {code}
#
# {tgt_lang} function:\"\"\""""
#
#         start_time = time.time()
#
#         inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.device)
#         output_ids = self.model.generate(
#             input_ids=inputs["input_ids"],
#             attention_mask=inputs["attention_mask"],
#             max_new_tokens=max_new_tokens,
#             num_beams=5,
#             early_stopping=True,
#             do_sample=False,
#             pad_token_id=self.tokenizer.pad_token_id
#         )
#
#         elapsed = time.time() - start_time
#         translated_code = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
#
#         # Remove the prompt from output
#         translated_code = translated_code.replace(prompt, "").strip()
#         translated_code = translated_code.split("\n\n")[0]  # keep only the first function
#
#         return {
#             "code": translated_code,
#             "time": elapsed
#         }






import time
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class CodeGenWrapper:
    def __init__(self, model_name="Salesforce/codegen-350M-multi", device=None):
        """
        Initialize CodeGen model and tokenizer.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

        # Set padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Device setup
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def extract_java_logic(self, java_code):
        """
        Extract the main logic inside Java main method or first function.
        """
        # Extract content inside main method if present
        main_match = re.search(r'public static void main\s*\(.*?\)\s*\{(.*)\}', java_code, re.DOTALL)
        if main_match:
            logic = main_match.group(1)
        else:
            # Fallback: use everything inside class
            class_match = re.search(r'public class .*?\{(.*)\}', java_code, re.DOTALL)
            logic = class_match.group(1) if class_match else java_code
        return logic.strip()

    def translate(self, java_code, src_lang="Java", tgt_lang="Python", max_new_tokens=256):
        """
        Translate Java code to Python using CodeGen.
        Returns translated code and elapsed time.
        """
        java_logic = self.extract_java_logic(java_code)

        prompt = f"""Translate the following {src_lang} code into {tgt_lang}:

### {src_lang}
{java_logic}

### {tgt_lang}
"""

        start_time = time.time()

        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.device)
        output_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=5,
            early_stopping=True,
            pad_token_id=self.tokenizer.pad_token_id
        )

        elapsed = time.time() - start_time
        decoded = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Extract only the tgt_lang part
        if f"### {tgt_lang}" in decoded:
            translated_code = decoded.split(f"### {tgt_lang}", 1)[1].strip()
            # cut off if the model repeats source tag again
            if f"### {src_lang}" in translated_code:
                translated_code = translated_code.split(f"### {src_lang}", 1)[0].strip()
        else:
            translated_code = decoded.strip()

        return {
            "code": translated_code,
            "time": elapsed
        }

# 🔹 Usage example
if __name__ == "__main__":
    wrapper = CodeGenWrapper()

    java_code = """
import java.util.Scanner;

public class EvenOrOdd {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int number = scanner.nextInt();
        if (number % 2 == 0) {
            System.out.println(number + " is an even number.");
        } else {
            System.out.println(number + " is an odd number.");
        }
        scanner.close();
    }
}
"""

    result = wrapper.translate(java_code)
    print("=== Translated Python Code ===\n")
    print(result["code"])
