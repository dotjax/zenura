from modules.io.text.tencode import text_to_bytes
from modules.io.text.tdecode import bytes_to_text
from modules.language.record import analyze_and_store_language
from modules.language.engine import Engine

def main():
    print("Type text to encode, analyze, and store. Type 'exit' to quit.\n")
    engine = Engine()

    while True:
        user_text = input("Enter text: ")
        if user_text.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        if not user_text.strip():
            print("Empty input detected. Try entering real text.\n")
            continue

        encoded_bytes = text_to_bytes(user_text)
        print(f"\nEncoded Bytes: {encoded_bytes}")

        decoded_text = bytes_to_text(encoded_bytes)
        print(f"Decoded Text: {decoded_text}\n")

        analyze_and_store_language(user_text)

        word_values = list(user_text.encode("utf-8"))
        delta8 = [word_values[i] - word_values[i - 1] for i in range(1, len(word_values))]
        xor8 = [format(word_values[i] ^ word_values[i - 1], "08b") for i in range(1, len(word_values))]

        ai_response = engine.generate(user_text, word_values, delta8, xor8)
        print(f"AI Response: {ai_response}\n")

if __name__ == "__main__":
    main()