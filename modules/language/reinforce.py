# modules/learning/reinforce.py
# Reinforces dominant predictions in 8-bit memory

import os
import importlib.util
from collections import defaultdict

def load_memory(file_path):
    spec = importlib.util.spec_from_file_location("learned", file_path)
    learned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(learned)
    return learned.memory

def save_memory(file_path, memory):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("# Reinforced memory\nmemory = {\n")
        for key, outcomes in memory.items():
            f.write(f"    {key}: {outcomes},\n")
        f.write("}\n")
    print(f"Reinforced and saved: {file_path}")

def reinforce_dominant(memory, factor=2):
    new_memory = defaultdict(dict)
    for pattern, outcomes in memory.items():
        if not outcomes:
            continue
        dominant = max(outcomes, key=outcomes.get)
        for val, count in outcomes.items():
            if val == dominant:
                new_memory[pattern][val] = count + factor
            else:
                new_memory[pattern][val] = count
    return new_memory

def reinforce_file(file_path, factor=2):
    memory = load_memory(file_path)
    reinforced = reinforce_dominant(memory, factor=factor)
    save_memory(file_path, reinforced)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python reinforce.py <path_to_learned_file> [factor]")
        sys.exit(1)
    path = sys.argv[1]
    factor = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    reinforce_file(path, factor)
