from pathlib import Path
from time import sleep
from modules.language.core.memory import saving
from modules.language.core.algorithms.basic import delta
from modules.language.core.algorithms.basic import byte
from modules.language.core.algorithms.basic import xor

INPUT_DIR = Path("data/neural/language/input/user")
OUTPUT_DIR = Path("data/neural/language/learned/delta")

def run():
    print("Daemon activated. Listening to memory...")
    processed = set()

    while True:
        for file in INPUT_DIR.glob("*.py"):
            if file.name in processed:
                continue

            try:
                content = file.read_text()
                local_vars = {}
                exec(content, {}, local_vars)
                data = local_vars.get("analyzed")

                if data:
                    result = delta.train(data)
                    saving.write_learned(result, OUTPUT_DIR)
                    processed.add(file.name)
            except Exception as e:
                print(f"Error processing {file.name}: {e}")
        sleep(15)

if __name__ == "__main__":
    run()
