from datetime import datetime
from pathlib import Path

def write_input(data, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_input_{timestamp}.py"
    full_path = Path(base_path) / filename
    full_path.write_text(f"analyzed = {repr(data)}\n")
    return str(full_path)

def write_learned(data, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"learned_delta_{timestamp}.py"
    full_path = Path(base_path) / filename
    full_path.write_text(f"learned = {repr(data)}\n")
    return str(full_path)
