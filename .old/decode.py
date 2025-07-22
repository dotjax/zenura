import os
import importlib.util
from datetime import datetime


def load_latest_learned_memory(directory="data/neural/language/algorithm"):
    files = sorted(
        (f for f in os.listdir(directory) if f.endswith(".py") and f.startswith("learned_")),
        key=lambda f: os.path.getmtime(os.path.join(directory, f)),
        reverse=True
    )
    if not files:
        print("No learned memory files found.")
        return {}

    path = os.path.join(directory, files[0])
    print(f"Decoding from latest memory file: {files[0]}")
    spec = importlib.util.spec_from_file_location("learned", path)
    learned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(learned)
    return learned.memory


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

    text_bytes.append(next_byte)

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


def generate_and_save_output():
    memory = load_latest_learned_memory()
    if not memory:
        return "[No learned memory to decode.]"
    decoded_text, text_bytes, delta_values, xor_values, analysis_lines = decode_learned_memory(memory)
    save_output(decoded_text, text_bytes, delta_values, xor_values, analysis_lines)
    return decoded_text


if __name__ == "__main__":
    generate_and_save_output()
