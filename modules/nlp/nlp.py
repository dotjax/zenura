from datetime import datetime
from pathlib import Path

def analyze_text_signal(text, source='user'):
    if not text.strip():
        return None

    timestamp = datetime.utcnow().isoformat()
    byte_values = list(text.encode('utf-8'))
    delta_profile = []
    xor_trace = []
    prev = None

    for b in byte_values:
        if prev is not None:
            delta_profile.append(b - prev)
            xor_trace.append(bin(b ^ prev)[2:].zfill(8))
        prev = b

    entropy = entropy_8bit(byte_values)

    memory = {
        "text": text,
        "source": source,
        "created": timestamp,
        "byte_values": byte_values,
        "delta_profile": delta_profile,
        "xor_trace": xor_trace,
        "entropy": entropy
    }

    store_memory(memory, text, timestamp)
    return memory

def entropy_8bit(byte_values):
    total = len(byte_values)
    if total == 0:
        return 0
    freq = {}
    for b in byte_values:
        freq[b] = freq.get(b, 0) + 1
    entropy_raw = 0
    for c in freq.values():
        p = (c * 256) // total
        entropy_raw += p * (256 - p)
    entropy_scaled = entropy_raw // total
    return min(entropy_scaled, 255)

def store_memory(data, word, timestamp):
    path = Path("data/nlp/")
    path.mkdir(parents=True, exist_ok=True)
    word_safe = "".join(c if c.isalnum() else "_" for c in word)
    fname = f"{timestamp.replace(':','-')}_{word_safe}.py"
    with open(path / fname, "w") as f:
        f.write(f"text = {repr(data['text'])}\n")
        f.write(f"source = {repr(data['source'])}\n")
        f.write(f"created = {repr(data['created'])}\n")
        f.write(f"byte_values = {data['byte_values']}\n")
        f.write(f"delta_profile = {data['delta_profile']}\n")
        f.write(f"xor_trace = {data['xor_trace']}\n")
        f.write(f"entropy = {data['entropy']}\n")