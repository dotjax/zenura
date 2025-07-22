# modules/language/algorithms/controller.py

# Import the other algorithm modules from the same package
from . import map
from . import clusterer

def run_pipeline():
    """
    Orchestrates the entire learning and generalization pipeline.
    This is the main entry point for processing. It updates the global
    memory in the 'map' module with the final, generalized result.
    """
    print("--- Starting Learning Pipeline ---")

    # Step 1: Build the raw memory map from all input files.
    # This calls the process() function from your map.py file, which
    # populates the global 'map.memory' dictionary.
    print("\n[Phase 1: Mapping raw patterns...]")
    map.process()
    print(f"[Phase 1 Complete: {len(map.memory)} raw patterns found.]")

    # Step 2: Apply the clustering algorithm to generalize the memory.
    # This takes the memory from map.py, processes it, and returns
    # a new, generalized version.
    print("\n[Phase 2: Clustering and generalizing patterns...]")
    generalized_memory = clusterer.generalize(map.memory)
    print(f"[Phase 2 Complete: {len(generalized_memory)} generalized patterns created.]")

    # Step 3: Update the main memory with the final, generalized version.
    # This is a critical step. It ensures that any other part of the program
    # that accesses 'map.memory' will get the fully processed data.
    map.memory = generalized_memory
    print("\n--- Learning Pipeline Finished ---\n")

# This part allows you to test the controller directly if you ever need to.
if __name__ == '__main__':
    run_pipeline()
