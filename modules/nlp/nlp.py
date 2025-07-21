from datetime import datetime
from pathlib import Path
import math
from typing import Any, Mapping

def analyze_text_signal(text, source='user'):
    if not text.strip():
        return None

    # timestamp and raw 16-bit code units (UTF-16BE, no BOM)
    timestamp = datetime.utcnow().isoformat()
    raw = text.encode('utf-16-be')
    words16 = list(memoryview(raw).cast('H'))

    # build 16-bit delta and XOR traces
    delta_profile = []
    xor_trace     = []
    prev = None
    for w in words16:
        if prev is not None:
            delta_profile.append(w - prev)
            xor_trace.append(format(w ^ prev, '016b'))
        prev = w

    # compute true Shannon entropy over 16-bit symbols, scaled 0–65535
    entropy = entropy_16bit(words16)

    memory = {
        "text":        text,
        "source":      source,
        "created":     timestamp,
        "word_values": words16,
        "delta16":     delta_profile,
        "xor16":       xor_trace,
        "entropy16":   entropy
    }

    store_memory(memory, text, timestamp)
    return memory

def entropy_16bit(words16):
    total = len(words16)
    if total == 0:
        return 0

    # count frequencies
    freq = {}
    for w in words16:
        freq[w] = freq.get(w, 0) + 1

    # Shannon entropy in bits
    H = 0.0
    for count in freq.values():
        p = count / total
        H -= p * math.log2(p)

    # H ranges from 0 to 16 bits → scale into [0, 65535]
    return int((H / 16) * 65535)

# ──────────────────────────────────────────────────────────────────────────
def _render_class(name: str, attrs: Mapping[str, Any]) -> str:
    """
    Render `attrs` into a simple Python class called `name`.
    Ensures long lists are written in full, not truncated.
    """
    lines = [f"class {name}:"]
    lines.append('    """Auto-generated memory record."""')
    lines.append("    def __init__(self):")

    if not attrs:
        lines.append("        pass")
    else:
        for k, v in attrs.items():
            # pretty-print long lists / tuples without truncation
            if isinstance(v, (list, tuple)) and len(v) > 20:
                elems = ",\n".join(" " * 12 + repr(item) for item in v)
                v_repr = "[\n" + elems + "\n" + " " * 8 + "]"
            else:
                v_repr = repr(v)

            lines.append(f"        self.{k} = {v_repr}")

    lines.append("")  # trailing newline
    return "\n".join(lines)
# ──────────────────────────────────────────────────────────────────────────
def _render_flat(attrs: Mapping[str, Any]) -> str:
    """
    Render `attrs` as plain assignments, one per line.
    """
    lines = []
    for k, v in attrs.items():
        lines.append(f"{k:<12} = {repr(v)}")
    lines.append("")            # trailing newline
    return "\n".join(lines)
# ──────────────────────────────────────────────────────────────────────────

def store_memory(data, word, timestamp):
    path = Path("data/nlp/")
    path.mkdir(parents=True, exist_ok=True)
    word_safe = "".join(c if c.isalnum() else "_" for c in word)
    fname = f"{timestamp.replace(':','-')}_{word_safe}.py"

    class_src = _render_class("MemoryRecord", data)  # use class renderer
    with open(path / fname, "w", encoding="utf-8") as f:
        f.write(class_src)