def learn_frequency(byte_input):
    freq = [0] * 256
    for b in byte_input:
        freq[b] = min(freq[b] + 1, 255)
    return freq


def learn_delta(byte_input):
    delta = [0] * 256
    for i in range(1, len(byte_input)):
        d = (byte_input[i] - byte_input[i - 1]) % 256
        delta[d] = min(delta[d] + 1, 255)
    return delta

def learn_xor(byte_input):
    xor = [0] * 256
    for i in range(1, len(byte_input)):
        x = byte_input[i] ^ byte_input[i - 1]
        xor[x] = min(xor[x] + 1, 255)
    return xor

def evaluate_entropy(byte_input):
    seen = [0] * 256
    unique = 0
    delta_sum = 0
    for i in range(len(byte_input)):
        b = byte_input[i]
        if seen[b] == 0:
            seen[b] = 1
            unique += 1
        if i > 0:
            delta_sum += abs(b - byte_input[i - 1])
    avg_delta = delta_sum // max(len(byte_input) - 1, 1)
    return min(unique * avg_delta, 255)

def learn_ngrams(byte_input):
    memory = {}
    for i in range(len(byte_input) - 2):
        key = (byte_input[i], byte_input[i + 1])
        val = byte_input[i + 2]
        if key not in memory:
            memory[key] = val
    return memory

def learn_rules(observed):
    rules = []  # Or load existing set
    for x, y, z in observed:  # triple input
        # Apply rule format: if (x op y == target) then z satisfies condition
        # Mutate strength based on correctness
        pass  # You already have this structure
    return rules

def evaluate_confidence(entropy_score, rule_matches):
    base = entropy_score
    if rule_matches < 2:
        base -= 32
    return max(min(base, 255), 0)

def reduce_patterns(byte_input):
    patterns = []
    for i in range(len(byte_input) - 2):
        if byte_input[i] == byte_input[i + 1]:
            patterns.append((byte_input[i], i))
    return patterns

def learn_temporal(byte_input, memory, tick):
    for b in byte_input:
        memory[b] = tick
    return memory

def classify_bitfield(byte_input):
    fields = [0] * 8
    for b in byte_input:
        for i in range(8):
            if (b >> i) & 1:
                fields[i] += 1
    return fields

def mutate_rules(rules, confidence):
    if confidence < 64:
        # Try mutating target value or logic operator
        pass  # hook into existing mutation logic
    return rules

{
    "frequency": [...],
    "delta": [...],
    "xor": [...],
    "entropy": 123,
    "ngrams": { (x, y): z },
    "rules": [...],
    "confidence": 200,
    "temporal": {...},
    "bitfields": [...],
    "patterns": [...]
}

layered/
├── learn.py                        # Main orchestrator
├── frequency.py                   # Tracks byte counts
├── delta.py                       # Tracks byte deltas
├── xor.py                         # XOR transitions
├── entropy.py                     # Approximates disorder
├── sequence.py                    # N-gram engine
├── rules.py                       # Arithmetic symbolic rules
├── confidence.py                  # Trust scoring
├── pattern.py                     # Pattern reduction logic
├── temporal.py                    # Memory decay + tick system
├── bitfield.py                    # Bitwise classification
├── mutate.py                      # Handles rule mutation triggers

from . import frequency, delta, xor, entropy, sequence, rules
from . import confidence, pattern, temporal, bitfield, mutate

def learn(analyzed, tick=0, temporal_memory=None):
    byte_input = analyzed["analysis"]["byte"]

    output = {
        "frequency": frequency.learn(byte_input),
        "delta": delta.learn(byte_input),
        "xor": xor.learn(byte_input),
        "entropy": entropy.evaluate(byte_input),
        "ngrams": sequence.learn(byte_input),
        "rules": rules.learn(byte_input),
        "bitfields": bitfield.classify(byte_input),
        "patterns": pattern.reduce(byte_input),
        "temporal": temporal.learn(byte_input, temporal_memory, tick),
    }

    output["confidence"] = confidence.evaluate(
        output["entropy"], len(output["rules"])
    )

    output["rules"] = mutate.adapt(output["rules"], output["confidence"])

    return output

data/neural/language/output/self/learned_unified_<timestamp>.py

learned = {
    "frequency": [...],
    "delta": [...],
    ...
}

