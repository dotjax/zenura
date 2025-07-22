def generalize(memory, byte_tolerance=2, delta_tolerance=2, xor_tolerance=2):
    """
    Optimized function to generalize memory by clustering patterns.
    """
    # Step 1: Group all patterns into clusters to avoid redundant comparisons.
    clusters = {}
    
    # Use the tolerances to define the 'bin' size for clustering.
    # A larger tolerance creates larger, broader bins.
    byte_bin = byte_tolerance * 2 + 1
    delta_bin = delta_tolerance * 2 + 1
    xor_bin = xor_tolerance * 2 + 1

    for pattern in memory.keys():
        # Assign each pattern to a cluster key based on its binned values.
        cluster_key = (
            round(pattern[0] / byte_bin),
            round(pattern[1] / delta_bin),
            round(pattern[2] / xor_bin)
        )
        if cluster_key not in clusters:
            clusters[cluster_key] = []
        clusters[cluster_key].append(pattern)

    # Step 2: Process each cluster to create the generalized memory.
    generalized = {}
    for cluster_key, patterns_in_cluster in clusters.items():
        # For each pattern in the cluster, merge its outcomes into a single dict.
        merged_outcomes = {}
        for pattern in patterns_in_cluster:
            for pred, count in memory[pattern].items():
                merged_outcomes[pred] = merged_outcomes.get(pred, 0) + count
        
        # Use a representative pattern from the cluster as the new key.
        # Here, we just use the first one.
        representative_pattern = patterns_in_cluster[0]
        generalized[representative_pattern] = merged_outcomes

    return generalized

if __name__ == "__main__":
    # Quick self-test
    sample_memory = {
        (100, 0, 0): {101: 10, 102: 2},
        (101, 1, 0): {102: 5},
        (99, -1, 1): {100: 3},
        (200, 50, 50): {201: 8}, # A separate cluster
        (201, 51, 49): {202: 12}  # Belongs to the same cluster as above
    }
    gen = generalize(sample_memory)
    print("Generalized memory:")
    for k, v in gen.items():
        print(f"{k}: {v}")