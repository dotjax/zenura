from datetime import datetime
from pathlib import Path
from modules.language.core.algorithms.basic import byte, delta, xor

def train(memory):
    # Train all three algorithms on the same memory
    byte.train(memory)
    delta.train(memory)
    xor.train(memory)

    # Retrieve internal memory states
    byte_elements = byte.elements
    delta_elements = delta.elements
    xor_elements = xor.elements

    # Fuse their outputs into 16-bit capped values
    fused = [0] * 65536
    for i in range(65536):
        fused[i] = min(byte_elements[i] + delta_elements[i] + xor_elements[i], 65535)

    # Include source input as traceable metadata
    source = memory["metadata"].get("source", "")
    save(fused, byte_elements, delta_elements, xor_elements, source)

def save(fused, byte_elements, delta_elements, xor_elements, source):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def write_file(subfolder, filename, data, label):
        path = Path("data/neural/language/learned") / subfolder / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Auto-generated {label} neural file\n")
            if source:
                safe_source = source.replace('"', '\\"')
                f.write(f"# Source: \"{safe_source}\"\n")
            f.write("elements = [\n")
            for i in range(0, 65536, 8):
                row = ", ".join(str(data[j]) for j in range(i, i+8))
                f.write(f"    {row},\n")
            f.write("]\n")

    write_file("byte", f"byte_neural_{timestamp}.py", byte_elements, "byte")
    write_file("delta", f"delta_neural_{timestamp}.py", delta_elements, "delta")
    write_file("xor", f"xor_neural_{timestamp}.py", xor_elements, "xor")
    write_file("layered", f"layered_neural_{timestamp}.py", fused, "layered fusion")
