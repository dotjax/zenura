from modules.language.encode import text_to_file
from modules.language import algorithm, generator

def interactive_loop():
    print("Type text to encode, learn, respond, and save. Type 'exit' to quit.\n")
    
    input_dir = "data/neural/language/input/user"
    output_dir = "data/neural/language/output/generated"
    
    while True:
        try:
            user_input = input("Enter text: ").strip()
            
            if user_input.lower() in {"exit", "quit"}:
                print("Exiting...")
                break

            if not user_input:
                print("Empty input detected. Try again.\n")
                continue

            text_to_file(user_input, input_dir, "text_", show_analysis=True)
            algorithm.process()
            generated_bytes = generator.generate_response(algorithm.memory)
            
            if generated_bytes:
                response = bytes(generated_bytes).decode('utf-8', errors='ignore')
                text_to_file(response, output_dir, "response_", show_analysis=False)
                print(f"Response: {response}\n")
            else:
                print("Response: (Could not generate a response from current memory)\n")

        except KeyboardInterrupt:
            print("\n[Interrupted] Exiting...\n")
            break

def main():
    interactive_loop()

if __name__ == "__main__":
    main()