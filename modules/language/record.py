import os
from datetime import datetime

def render_language_class(name: str, attrs: dict) -> str:
    lines = [f"class {name}:"]
    lines.append('    """Auto-generated language record."""')
    lines.append("    def __init__(self):")
    for key, value in attrs.items():
        lines.append(f"        self.{key} = {repr(value)}")
    return "\n".join(lines)

def analyze_and_store_language(text: str) -> None:
    raw = text.encode('utf-8')
    words8 = list(raw)

    delta_profile = [words8[i] - words8[i - 1] for i in range(1, len(words8))]
    xor_trace = [format(words8[i] ^ words8[i - 1], '08b') for i in range(1, len(words8))]

    timestamp = datetime.utcnow().isoformat().replace(':', '-')
    word_safe = "".join(c if c.isalnum() else "_" for c in text)[:10]
    fname = f"{timestamp}_{word_safe or 'unknown'}.py"

    language_data = {
        "text": text,
        "created": timestamp,
        "word_values": words8,
        "delta8": delta_profile,
        "xor8": xor_trace,
    }

    # Ensure directory exists
    output_dir = os.path.join("data", "input")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, fname)

    # Generate and save the class file
    class_code = render_language_class("LanguageRecord", language_data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(class_code)