"""
Light-weight semantic similarity engine.

Functions
---------
build_signature(record)     -> dict[str, int|float]
distance(sigA, sigB)        -> float
load_corpus(path)           -> list[(sig, MemoryRecord)]
nearest(text, k=3)          -> list[(distance, MemoryRecord)]
"""

from pathlib import Path
from importlib.machinery import SourceFileLoader
from typing import List, Tuple, Dict, Any
from modules.nlp.nlp import analyze_text_signal
from datetime import datetime

# hand-tuned weights
_W1, _W2, _W3, _W4, _W5 = 3, 1, 2, 1, 1

# neuron storage path
_NEURON_PATH = Path("data/mem")
_NEURON_PATH.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────────────────────
def _bitcount(x: int) -> int:
    # Python ≥3.8 has int.bit_count()
    try:
        return x.bit_count()            # type: ignore[attr-defined]
    except AttributeError:
        return bin(x).count("1")

# ──────────────────────────────────────────────────────────────
def build_signature(src: Any) -> Dict[str, float]:
    """
    Accept MemoryRecord *instance* or plain dict produced by
    analyze_text_signal() and return its 5-scalar signature.
    """
    # normalize attribute access
    getter = src.get if isinstance(src, dict) else lambda k: getattr(src, k)

    word_values: List[int] = getter("word_values")
    delta16:     List[int] = getter("delta16")
    xor16:       List[str] = getter("xor16")

    n_words     = len(word_values)
    avg_word    = sum(word_values) / n_words if n_words else 0
    first_delta = delta16[0] if delta16 else 0
    entropy16   = getter("entropy16")
    xor_bits    = int(xor16[0], 2) if xor16 else 0

    return dict(
        n_words=n_words,
        avg_word=avg_word,
        first_delta=first_delta,
        entropy16=entropy16,
        xor_bits=xor_bits,
    )

# ──────────────────────────────────────────────────────────────
def distance(a: Dict[str, float], b: Dict[str, float]) -> float:
    """
    Weighted L1 + Hamming distance on the 5-element signatures.
    """
    return (
        abs(a["n_words"]   - b["n_words"])   * _W1 +
        abs(a["avg_word"]  - b["avg_word"])  * _W2 +
        abs(a["first_delta"] - b["first_delta"]) * _W3 +
        abs(a["entropy16"] - b["entropy16"]) * _W4 +
        _bitcount(a["xor_bits"] ^ b["xor_bits"]) * _W5
    )

# ──────────────────────────────────────────────────────────────
def save_neuron(signature: Dict[str, float], text: str) -> None:
    """
    Save computed signature as executable Python code in data/mem/.
    """
    timestamp = datetime.utcnow().isoformat().replace(':', '-')
    word_safe = "".join(c if c.isalnum() else "_" for c in text)[:10] or "unknown"
    fname = f"{timestamp}_{word_safe}.mem.py"
    
    lines = []
    lines.append("# Auto-generated neuron (signature)")
    lines.append("")
    for k, v in signature.items():
        lines.append(f"{k:<12} = {repr(v)}")
    lines.append("")
    
    with open(_NEURON_PATH / fname, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def _load_module(path: Path):
    name = path.stem
    loader = SourceFileLoader(name, str(path))
    return loader.load_module()          # type: ignore[deprecated-method]

def load_neurons() -> List[Tuple[Dict[str, float], str]]:
    """
    Load all .mem.py neuron files, return list of (signature_dict, filename).
    """
    neurons = []
    for p in _NEURON_PATH.glob("*.mem.py"):
        mod = _load_module(p)
        # Extract the signature values from the module
        sig = {}
        for attr in ['n_words', 'avg_word', 'first_delta', 'entropy16', 'xor_bits']:
            if hasattr(mod, attr):
                sig[attr] = getattr(mod, attr)
        if sig:  # only add if we found signature data
            neurons.append((sig, p.name))
    return neurons

# ──────────────────────────────────────────────────────────────
def load_corpus(path: Path = Path("data/nlp")) -> List[Tuple[Dict[str, float], Any]]:
    """
    Scan `path` for *.py memories, return list of (signature, MemoryRecord).
    """
    corpus = []
    for p in path.glob("*.py"):
        mod = _load_module(p)
        if hasattr(mod, "MemoryRecord"):
            rec = mod.MemoryRecord()
            corpus.append((build_signature(rec), rec))
    return corpus

# ──────────────────────────────────────────────────────────────
def analyze_and_store_neuron(text: str, source: str = 'user') -> Dict[str, float]:
    """
    Analyze text, build signature, and automatically save as neuron.
    Returns the computed signature.
    """
    memory_data = analyze_text_signal(text, source)
    signature = build_signature(memory_data)
    save_neuron(signature, text)
    return signature

def nearest(text: str, k: int = None) -> List[Tuple[float, Any]]:
    """
    Compute signature for `text`, compare against saved neurons,
    and return the k nearest matches. If k=None, return all.
    """
    memory_data = analyze_text_signal(text, source="query")
    fresh_sig = build_signature(memory_data)
    
    # Save this signature as a neuron
    save_neuron(fresh_sig, text)
    
    matches = []
    # Compare against existing neurons
    for sig, filename in load_neurons():
        matches.append((distance(fresh_sig, sig), filename))
    matches.sort(key=lambda t: t[0])
    
    if k is None:
        return matches
    return matches[:k]  #
