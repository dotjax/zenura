def text_to_bytes(text=None):
    if text is None:
        text = input("Enter text: ")
    
    byte_data = text.encode('utf-8')

    print("\nASCII Analysis:")
    prev_char = None
    for char in text:
        curr_byte = ord(char)
        print(f"{char}: {curr_byte} (dec) = {bin(curr_byte)[2:].zfill(8)} (bin)")
        if prev_char:
            diff = curr_byte - ord(prev_char)
            xor = curr_byte ^ ord(prev_char)
            print(f"  Δ from {prev_char}: {diff} steps")
            print(f"  XOR pattern: {bin(xor)[2:].zfill(8)}")
        prev_char = char

    return list(byte_data)

if __name__ == "__main__":
    byte_output = text_to_bytes()
    print(f"\nRaw bytes: {bytes(byte_output)}")
    print(f"Byte values: {byte_output}")