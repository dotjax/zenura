import os
import importlib


def generalize_all(memory):
    """
    Calls all generalizer modules in ./galgorithms and returns combined generalized memory.
    Each submodule must define a function: generalize(memory)
    """
    generalized = {}
    base_dir = os.path.dirname(__file__)
    galgo_path = os.path.join(base_dir, "galgorithms")

    for fname in os.listdir(galgo_path):
        if fname.endswith(".py") and not fname.startswith("__"):
            mod_name = fname[:-3]
            import_path = f"modules.language.galgorithms.{mod_name}"

            try:
                module = importlib.import_module(import_path)
                if hasattr(module, "generalize"):
                    print(f"Applying generalizer: {mod_name}")
                    result = module.generalize(memory)
                    for key, outcomes in result.items():
                        if key not in generalized:
                            generalized[key] = outcomes
                        else:
                            for val, count in outcomes.items():
                                generalized[key][val] = generalized[key].get(val, 0) + count
                else:
                    print(f"Skipping {mod_name}: No generalize() function found.")
            except Exception as e:
                print(f"Error loading {mod_name}: {e}")

    return generalized


if __name__ == "__main__":
    from modules.language.algorithm import memory
    result = generalize_all(memory)
    print(f"Generalized patterns: {len(result)}")
