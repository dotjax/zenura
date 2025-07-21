import os
import importlib.util
from datetime import datetime


def load_all_learned_memory(directory="data/neural/language"):
    memory = {}
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename.startswith("learned_"):
            path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location("learned", path)
            learned = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(learned)
            local_mem = learned.memory
            for key, outcomes in local_mem.items():
                if key not in memory:
                    memory[key] = outcomes
                else:
                    for val, count in outcomes.items():
                        memory[key][val] = memory[key].get(val, 0) + count
    return memory


def decode_learned_memory(memory):
    text_bytes = []
    delta_values = []
    xor_values = []
    analysis_lines = []
    zfill_w = 8

    for key, outcomes in memory.items():
        base = key[0]
        next_byte = max(outcomes, key=outcomes.get)
        text_bytes.append(base)
        delta_values.append(key[1])
        xor_values.append(key[2])

    # Add final predicted byte
    text_bytes.append(next_byte)

    # Build analysis
    prev_unit = None
    for unit in text_bytes:
        char = chr(unit)
        analysis_lines.append(f'{char}: {unit} (dec) = {bin(unit)[2:].zfill(zfill_w)} (bin)')
        if prev_unit is not None:
            diff = unit - prev_unit
            xorv = unit ^ prev_unit
            analysis_lines.append(f'  Delta from {chr(prev_unit)}: {diff} steps')
            analysis_lines.append(f'  XOR pattern: {bin(xorv)[2:].zfill(zfill_w)}')
        prev_unit = unit

    decoded_text = bytes(text_bytes).decode("utf-8", errors="replace")
    return decoded_text, text_bytes, delta_values, xor_values, analysis_lines


def save_output(decoded_text, text_bytes, delta_values, xor_values, analysis_lines):
    os.makedirs("data/output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/output/text_{timestamp}.py"

    file_content = f'''generated = "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
original_text = "{decoded_text}"
byte_count = {len(text_bytes)}

analysis = [
{chr(10).join(f'    "{line}",' for line in analysis_lines)}
]

text = """{decoded_text}"""
byte_values = {text_bytes}
encoding = "utf-8"
delta = {delta_values}
xor = {xor_values}
'''

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(file_content)

    print(f"\nSaved to: {filename}")
    print(f"Output Text: {decoded_text}")


if __name__ == "__main__":
    memory = load_all_learned_memory()
    decoded_text, text_bytes, delta_values, xor_values, analysis_lines = decode_learned_memory(memory)
    save_output(decoded_text, text_bytes, delta_values, xor_values, analysis_lines)
