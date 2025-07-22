from modules.language.processor import process
from modules.language.memory.python import write
from modules.language.memory.name import generate
from modules.language.dialogue import train_on_live_input

def main():
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
        print(f"Saved to {path}")

        train_on_live_input(result)

if __name__ == "__main__":
    main()
    