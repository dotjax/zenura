# main.py
from modules.io.tencode import text_to_bytes
from modules.io.tdecode import bytes_to_text
from modules.nlp.nlp import analyze_text_signal

def main():
    print("Byte-Native NLP Engine 🧠")
    print("Type text to encode, analyze, and store. Type 'exit' to quit.\n")

    while True:
        user_text = input("Enter text: ")
        if user_text.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        if not user_text.strip():
            print("🛑 Empty input detected. Try entering real text.\n")
            continue

        encoded_bytes = text_to_bytes(user_text)
        print(f"\nEncoded Bytes: {encoded_bytes}")

        decoded_text = bytes_to_text(encoded_bytes)
        print(f"Decoded Text: {decoded_text}\n")

        print("Saving semantic memory...")
        analyze_text_signal(user_text, source='user')
        print("✔ Memory saved.\n")

if __name__ == "__main__":
    main()