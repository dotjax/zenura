def coalesce(memory_dicts):
    """
    Coalesce multiple memory dictionaries into one unified neural network.
    
    Args:
        memory_dicts: List of (algorithm_name, memory_dict) tuples
        
    Returns:
        Unified memory dictionary with all patterns merged and weighted
    """
    unified_memory = {}
    
    # Algorithm weights (can be adjusted based on algorithm importance)
    algorithm_weights = {
        'map': 1.0,           # Raw patterns
        'clusterer': 1.5,     # Generalized patterns (slightly higher weight)
        'semantic': 1.2,      # Semantic data (concept understanding)
        # Future algorithms can be added here
    }
    
    for algorithm_name, memory in memory_dicts:
        weight = algorithm_weights.get(algorithm_name, 1.0)
        
        for pattern, outcomes in memory.items():
            if pattern not in unified_memory:
                unified_memory[pattern] = {}
            
            # Merge outcomes with algorithm weighting
            for outcome, count in outcomes.items():
                weighted_count = count * weight
                unified_memory[pattern][outcome] = unified_memory[pattern].get(outcome, 0) + weighted_count
    
    return unified_memory



def save_coalesced_memory(memory, timestamp=None):
    """
    Save the coalesced memory to a file.
    """
    import os
    from datetime import datetime
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_dir = "data/neural/language/learned"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"learned_coalescer_{timestamp}.py"
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Coalesced neural network memory\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Algorithm: coalescer\n")
        f.write("# Description: Unified memory from all algorithms\n\n")
        f.write("memory = {\n")
        for key, outcomes in memory.items():
            f.write(f"    {key}: {outcomes},\n")
        f.write("}\n")
    
    print(f"Saved coalesced memory to {output_path}")
    return output_path

if __name__ == "__main__":
    # Quick self-test
    test_memories = [
        ('map', {
            (100, 0, 0): {101: 10, 102: 2},
            (101, 1, 0): {102: 5}
        }),
        ('clusterer', {
            (100, 0, 0): {101: 8, 103: 1},  # Overlapping pattern
            (200, 50, 50): {201: 8}          # New pattern
        }),
        ('semantic', {
            ('semantic_100_101', 0, 0): {101: 5},
            ('similar_100_101', 1, 1): {101: 8}
        })
    ]
    
    coalesced = coalesce(test_memories)
    print("Coalesced memory:")
    for k, v in coalesced.items():
        print(f"{k}: {v}") 