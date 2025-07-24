import os
from datetime import datetime

def write_input(data, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_input_{timestamp}.py"
    full_path = os.path.join(base_path, filename)

    with open(full_path, "w") as f:
        f.write(f"analyzed = {repr(data)}\n")

    return full_path

def write_learned(data, base_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"learned_delta_{timestamp}.py"
    full_path = os.path.join(base_path, filename)

    with open(full_path, "w") as f:
        f.write(f"learned = {repr(data)}\n")

    return full_path