import os
from datetime import datetime

# Import the algorithm modules from the same package
from . import map
from . import clusterer
from . import coalescer
from . import unifier

def save_algorithm_output(memory, algorithm_name):
    """
    Save algorithm output to data/neural/language/learned with algorithm label.
    """
    output_dir = "data/neural/language/learned"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"learned_{algorithm_name}_{timestamp}.py"
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Auto-generated learned memory\nmemory = {\n")
        for key, outcomes in memory.items():
            f.write(f"    {key}: {outcomes},\n")
        f.write("}\n")
    
    print(f"Saved {algorithm_name} output to {output_path}")

def run_pipeline():
    """
    Orchestrates the entire learning and generalization pipeline.
    Runs algorithms sequentially and saves outputs with algorithm labels.
    """
    print("--- Starting Learning Pipeline ---")

    print("\n[Mapping raw patterns...]")
    map.process()
    save_algorithm_output(map.memory, "map")
    print(f"[Complete: {len(map.memory)} raw patterns found.]")

    print("\n[Clustering and generalizing patterns...]")
    generalized_memory = clusterer.generalize(map.memory)
    save_algorithm_output(generalized_memory, "clusterer")
    print(f"[Complete: {len(generalized_memory)} generalized patterns created.]")

    print("\n[Coalescing unified neural network...]")
    memory_dicts = [
        ('map', map.memory),
        ('clusterer', generalized_memory),
    ]
    coalesced_memory = coalescer.coalesce(memory_dicts)
    coalescer.save_coalesced_memory(coalesced_memory)
    print(f"[Complete: {len(coalesced_memory)} unified patterns created.]")

    print("\n[Unifying with meta-analysis...]")
    unified_memory = unifier.unify(coalesced_memory)
    unifier.save_unified_memory(unified_memory)
    print(f"[Complete: Rich neural network with meta-analysis created.]")
    print("\n--- Learning Pipeline Finished ---\n")

# This part allows you to test the controller directly if you ever need to.
if __name__ == '__main__':
    run_pipeline()
