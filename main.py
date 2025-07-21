from modules.io.text.tencode import text_to_bytes
from modules.io.text.tdecode import bytes_to_text
from modules.language.encode import text_to_file
from modules.language import decode
from modules.language import algorithm

def main():
    print("Zenura v0.1 - Interactive 8-bit Learning AI")
    print("Type text to teach Zenura. Type 'exit' to quit.\n")

    while True:
        user_text = input("You: ")
        if user_text.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        if not user_text.strip():
            print("Empty input detected. Try entering real text.\n")
            continue

        # Save input to data/input
        text_to_file(user_text)

        # Train immediately on the new input
        algorithm.process()

        # Decode and respond with the learned memory
        memory = decode.load_all_learned_memory()
        decoded_text, text_bytes, delta_values, xor_values, analysis_lines = decode.decode_learned_memory(memory)
        print(f"\nZenura: {decoded_text}\n")

if __name__ == "__main__":
    main()