# evaluators/syntax_checker.py
import tempfile
import subprocess
import os

def check_syntax(code, lang="python"):
    if lang.lower() == "python":
        try:
            compile(code, "<string>", "exec")
            return True
        except Exception:
            return False

    elif lang.lower() == "java":
        try:
            # Save to a temporary .java file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as tmp_file:
                tmp_file.write(code.encode("utf-8"))
                tmp_file_path = tmp_file.name

            # Try compiling with javac
            result = subprocess.run(
                ["javac", tmp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode == 0
        except Exception:
            return False
        finally:
            # Clean up temporary file
            try:
                os.remove(tmp_file_path)
                class_file = tmp_file_path.replace(".java", ".class")
                if os.path.exists(class_file):
                    os.remove(class_file)
            except:
                pass
    else:
        raise ValueError(f"Unsupported language: {lang}")
