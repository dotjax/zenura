from datetime import datetime
from pathlib import Path

def analyze_and_store_language(text: str) -> None:
    lang_path = Path("data/language")
    lang_path.mkdir(parents=True, exist_ok=True)

    raw = text.encode('utf-8')
    words8 = list(raw)

    delta_profile = []
    xor_trace = []
    prev = None
    for w in words8:
        if prev is not None:
            delta_profile.append(w - prev)
            xor_trace.append(format(w ^ prev, '08b'))
        prev = w

    timestamp = datetime.utcnow().isoformat().replace(':', '-')
    word_safe = "".join(c if c.isalnum() else "_" for c in text)[:10] or "unknown"
    fname = f"{timestamp}_{word_safe}.nlp.py"

    language_data = {
        "text": text,
        "created": timestamp,
        "word_values": words8,
        "delta8": delta_profile,
        "xor8": xor_trace,
    }

    try:
        with open(lang_path / fname, "w", encoding="utf-8") as f:
            f.write(render_language_class("LanguageRecord", language_data))
        print(f"✔ Language saved to {lang_path / fname}")
    except Exception as e:
        print(f"❌ Failed to save language: {e}")

def render_language_class(name: str, attrs: dict) -> str:
    lines = [f"class {name}:"]
    lines.append('    """Auto-generated language record."""')
    lines.append("    def __init__(self):")

    for k, v in attrs.items():
        lines.append(f"        self.{k} = {repr(v)}")

    lines.append("")
    return "\n".join(lines)