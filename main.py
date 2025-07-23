import threading
from modules.language.core.autonomy import daemon
from modules.language.core.analysis.processor import process
from modules.language.core.memory.format import write
from modules.language.core.memory.user import generate
from modules.language.core.dialogue.live import learn

def main():
    # Start the background daemon
    daemon_thread = threading.Thread(target=daemon.run, daemon=True)
    daemon_thread.start()

    while True:
        text = input("Enter input (or type 'exit' to quit): ")

        if text.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        result = process(text)
        print(f"\nProcessed Result: {result}\n")

        filename = generate(prefix="user")
        path = f"data/neural/language/input/user/{filename}"
        write(result, path)
        print(f"Saved to {path}\n")

        learned_result = learn(result)
        print("Neural output: ", learned_result)
        print("")

if __name__ == "__main__":
    main()
    