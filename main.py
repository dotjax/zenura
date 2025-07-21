from modules.io.text.tencode import text_to_bytes
from modules.language.encode import text_to_file
from modules.language import algorithm
from modules.language.decode import generate_and_save_output

def interactive_loop():
    print("Type text to encode, learn, respond, and save. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("Enter text: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Exiting...")
                break
            if not user_input:
                print("Empty input detected. Try again.\n")
                continue

            # Save input to data/input/ (encoded .py format)
            text_to_file(user_input)

            # Learn from all input data and update memory
            algorithm.process()

            # Decode from learned memory and auto-save to data/output/
            response = generate_and_save_output()
            print(f"\nAI Response: {response}\n")

        except KeyboardInterrupt:
            print("\n[Interrupted] Exiting...\n")
            break

def main():
    interactive_loop()

if __name__ == "__main__":
    main()
