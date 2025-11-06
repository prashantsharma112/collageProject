import time
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class CodeT5Wrapper:
    def __init__(self, model_name="Salesforce/codet5-base", device="cpu"):
        """
        Wrapper for CodeT5 model (Hugging Face).
        :param model_name: Model name on Hugging Face hub
        :param device: "cpu" or "cuda"
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        self.device = device

    def translate(self, code: str, src_lang: str = "java", tgt_lang: str = "python"):
        """
        Translate code from src_lang to tgt_lang using CodeT5.
        Returns dict { "code": str, "time": float }
        """
        # Prompt style to guide CodeT5
        prompt = f"Translate {src_lang} code to {tgt_lang}:\n{code}\n{tgt_lang}:"

        start_time = time.time()

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=512,
            num_beams=5,
            early_stopping=True
        )
        elapsed = time.time() - start_time

        # Decode
        translated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        # Cleanup (remove ``` blocks if model adds them)
        translated_code = re.sub(r"^```[a-zA-Z]*\n", "", translated_code)
        translated_code = re.sub(r"```$", "", translated_code)
        translated_code = translated_code.strip()

        if not translated_code:
            raise ValueError("❌ Empty translation received from CodeT5.")

        return {
            "code": translated_code,
            "time": elapsed
        }
