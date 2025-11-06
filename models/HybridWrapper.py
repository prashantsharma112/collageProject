import time
import re
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration, AutoModelForCausalLM

# print("🔹 HybridWrapper module loaded")

def extract_python_code(text: str) -> str:
    if not text:
        return ""

    blocks = re.findall(r"```(?:python)?(.*?)```", text, re.DOTALL)
    if blocks:
        text = "\n\n".join(blocks).strip()

    code_start = re.search(r"(import\s+\w+|def\s+\w+\s*\(|class\s+\w+\s*:|if\s+__name__)", text)
    if code_start:
        text = text[code_start.start():]

    cleaned = []
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
            ]
        ):
            continue
        if line.strip().startswith(("/*", "//", "# +", "# -", "#!")):
            continue
        cleaned.append(line)

    return "\n".join(cleaned).strip()

class HybridWrapper:
    def __init__(self, device=None):
        # Force CPU usage to avoid GPU OOM
        device = "cpu"
        self.device = torch.device(device)
        print(f"🔸 Using device: {self.device}")

        # Load CodeT5 on CPU
        print("🔸 Loading CodeT5...")
        self.code_tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
        self.code_model = T5ForConditionalGeneration.from_pretrained(
            "Salesforce/codet5-base"
        ).to(self.device)
        print("✅ CodeT5 loaded")

        # Load StarCoder on CPU
        print("🔸 Loading StarCoder (this may take a while)...")
        self.gen_tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoderbase-1b")
        self.gen_model = AutoModelForCausalLM.from_pretrained(
            "bigcode/starcoderbase-1b"
        ).to(self.device)
        self.gen_tokenizer.pad_token = self.gen_tokenizer.eos_token
        self.gen_model.config.pad_token_id = self.gen_tokenizer.eos_token_id
        print("✅ StarCoder loaded")

    def translate(self, code: str, src_lang="java", tgt_lang="python"):
        start_time = time.time()

        # Step 1 — Summarize code using CodeT5
        summary_prompt = f"summarize this {src_lang} code briefly:"
        inputs = self.code_tokenizer(
            summary_prompt, code, return_tensors="pt",
            truncation=True, max_length=512
        ).to(self.device)
        with torch.no_grad():
            summary_ids = self.code_model.generate(**inputs, max_new_tokens=50)
        summary = self.code_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Step 2 — Build StarCoder prompt
        target_prompt = (
            f"Translate the following {src_lang} code to {tgt_lang}.\n"
            f"Here’s a brief summary to help you understand it:\n"
            f"{summary}\n\n"
            f"{code}\n\n# Translated {tgt_lang} code:\n"
        )

        # Step 3 — Generate translation
        gen_inputs = self.gen_tokenizer(
            target_prompt, return_tensors="pt",
            truncation=True, max_length=512
        ).to(self.device)
        with torch.no_grad():
            outputs = self.gen_model.generate(
                **gen_inputs,
                max_new_tokens=256,
                pad_token_id=self.gen_tokenizer.eos_token_id,
                temperature=0.4,
                top_p=0.9
            )

        raw_translated = self.gen_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        clean_translated = extract_python_code(raw_translated)

        elapsed = time.time() - start_time

        return {"code": clean_translated, "time": elapsed}


