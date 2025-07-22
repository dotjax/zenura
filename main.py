from modules.language.encode import text_to_file
# Import the new controller and the map module (to access its memory)
from modules.language.algorithms import controller, map
from modules.language import generator

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

            # This part remains the same
            text_to_file(user_input, input_dir, "text_", show_analysis=True)
            
            # Call the new controller to run the entire learning pipeline.
            # This will handle mapping, clustering, and updating the final memory.
            controller.run_pipeline()
            
            # The generator gets the final, processed memory from map.memory
            generated_bytes = generator.generate_response(map.memory)
            
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
    # Run the full pipeline once at the start to load all existing data
    print("[System starting... Initializing learning pipeline.]")
    controller.run_pipeline()
    print("[Initialization complete. Ready for input.]")
    interactive_loop()

if __name__ == "__main__":
    main()
