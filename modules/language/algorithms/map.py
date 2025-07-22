import os
import ast
import importlib.util
from datetime import datetime
from pathlib import Path

input_dir = "data/neural/language/input/user/"
output_dir = "data/neural/language/learned/"
os.makedirs(output_dir, exist_ok=True)

memory = {}

def load_input_file(path):
    """Load input file safely, handling binary number syntax issues."""
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    
    # Create a safe namespace with only the variables we need
    namespace = {}
    
    # Extract the byte_values, delta, and xor lists using ast
    try:
        # Parse the file content
        tree = ast.parse(data)
        
        # Find the assignments we need
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ['byte_values', 'delta', 'xor']:
                        # Safely evaluate the value
                        try:
                            value = ast.literal_eval(node.value)
                            namespace[target.id] = value
                        except (ValueError, SyntaxError):
                            print(f"Warning: Could not parse {target.id} in {path}")
                            continue
        
        return namespace
        
    except SyntaxError as e:
        print(f"Warning: Syntax error in {path}: {e}")
        # Fallback: try to extract just the byte_values using regex
        import re
        byte_match = re.search(r'byte_values\s*=\s*(\[.*?\])', data, re.DOTALL)
        delta_match = re.search(r'delta\s*=\s*(\[.*?\])', data, re.DOTALL)
        xor_match = re.search(r'xor\s*=\s*(\[.*?\])', data, re.DOTALL)
        
        if byte_match:
            try:
                namespace['byte_values'] = ast.literal_eval(byte_match.group(1))
            except:
                pass
        if delta_match:
            try:
                namespace['delta'] = ast.literal_eval(delta_match.group(1))
            except:
                pass
        if xor_match:
            try:
                namespace['xor'] = ast.literal_eval(xor_match.group(1))
            except:
                pass
        
        return namespace

def update_memory(byte_values, delta, xor):
    for i in range(1, len(byte_values)):
        pattern = (byte_values[i - 1], delta[i - 1], xor[i - 1])
        prediction = byte_values[i]
        if pattern not in memory:
            memory[pattern] = {}
        if prediction not in memory[pattern]:
            memory[pattern][prediction] = 0
        memory[pattern][prediction] += 1

def save_memory(filename, memory):
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Auto-generated learned memory\nmemory = {\n")
        for key, outcomes in memory.items():
            f.write(f"    {key}: {outcomes},\n")
        f.write("}\n")
    print(f"Saved learned memory to {output_path}")

def process():
    global memory  # Correct placement of global declaration

    for file in os.listdir(input_dir):
        if not file.endswith(".py"):
            continue
        filepath = os.path.join(input_dir, file)
        print(f"Training on: {filepath}")
        data = load_input_file(filepath)
        local_memory = {}

        byte_values = data.get("byte_values")
        delta = data.get("delta")
        xor = data.get("xor")

        if not (byte_values and delta and xor):
            print(f"Skipping incomplete file: {file}")
            continue

        for i in range(1, len(byte_values)):
            pattern = (byte_values[i - 1], delta[i - 1], xor[i - 1])
            prediction = byte_values[i]
            if pattern not in local_memory:
                local_memory[pattern] = {}
            if prediction not in local_memory[pattern]:
                local_memory[pattern][prediction] = 0
            local_memory[pattern][prediction] += 1

        base_name = Path(file).stem.replace("text_", "learned_")
        out_name = f"{base_name}.py"
        save_memory(out_name, local_memory)

        # Also update full memory for in-session decoding
        for k, v in local_memory.items():
            if k not in memory:
                memory[k] = v
            else:
                for pred, count in v.items():
                    memory[k][pred] = memory[k].get(pred, 0) + count

def predict(prev, delta, xor):
    key = (prev, delta, xor)
    if key in memory:
        prediction = max(memory[key], key=memory[key].get)
        confidence = memory[key][prediction]
        return prediction, confidence
    return None, 0

if __name__ == "__main__":
    process()
