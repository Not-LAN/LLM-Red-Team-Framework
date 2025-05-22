import os

def load_prompt(relative_path):
    full_path = os.path.join("prompts", relative_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read().strip()
