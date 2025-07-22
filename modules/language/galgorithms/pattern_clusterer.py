def generalize(memory, byte_tolerance=2, delta_tolerance=2, xor_tolerance=2):
    """
    Generalize memory by clustering patterns close in byte, delta, and xor values.
    Patterns within tolerance are merged with weighted counts.
    """
    generalized = {}

    patterns = list(memory.keys())

    for base_pattern in patterns:
        base_byte, base_delta, base_xor = base_pattern
        merged_counts = {}

        # Find similar patterns within tolerances
        similar_patterns = [
            p for p in patterns
            if abs(p[0] - base_byte) <= byte_tolerance
            and abs(p[1] - base_delta) <= delta_tolerance
            and abs(p[2] - base_xor) <= xor_tolerance
        ]

        # Merge outcome counts weighted by closeness (simple inverse distance)
        for p in similar_patterns:
            distance = abs(p[0] - base_byte) + abs(p[1] - base_delta) + abs(p[2] - base_xor)
            weight = 1 / (distance + 1)  # +1 to avoid division by zero

            for pred, count in memory[p].items():
                merged_counts[pred] = merged_counts.get(pred, 0) + count * weight

        # Normalize counts to integers (round and filter zeros)
        merged_counts = {k: int(round(v)) for k, v in merged_counts.items() if v >= 1}

        if merged_counts:
            generalized[base_pattern] = merged_counts

    return generalized


if __name__ == "__main__":
    # Quick self-test
    sample_memory = {
        (100, 0, 0): {101: 10, 102: 2},
        (101, 1, 0): {102: 5},
        (99, -1, 1): {100: 3},
    }
    gen = generalize(sample_memory)
    print("Generalized memory:")
    for k, v in gen.items():
        print(f"{k}: {v}")
