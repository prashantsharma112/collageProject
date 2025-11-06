import time
import re
import google.generativeai as genai

class GeminiWrapper:
    def __init__(self, api_key, model_name="gemini-2.0-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def translate(self, code, src_lang="java", tgt_lang="python"):
        """
        Sends code to Gemini for translation between programming languages.
        """
        prompt = f"""You are a code translation assistant.
Convert the following {src_lang} code into equivalent {tgt_lang} code.
Preserve logic and structure as much as possible.
Only return the translated code without explanation.

Source code:
```{src_lang}
{code}

"""

        # Measure time
        start_time = time.time()
        
        response = self.model.generate_content(prompt)
        elapsed = time.time() - start_time

        # Extract plain text output
        translated_code = response.text.strip()

        # Remove triple backticks and language tags if present
        translated_code = re.sub(r"^```[a-zA-Z]*\n", "", translated_code)
        translated_code = re.sub(r"```$", "", translated_code)
        translated_code = translated_code.strip()

        # Validate output
        if not translated_code:
            raise ValueError("❌ Empty translation received from Gemini API.")

        return {
            "code": translated_code,
            "time": elapsed
        }
