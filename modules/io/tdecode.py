def bytes_to_text(byte_values, verbose=True):
    byte_data = bytes(byte_values)

    if verbose:
        print("\nASCII Analysis:")
        prev_byte = None
        for byte in byte_values:
            char = chr(byte)
            print(f"{byte} (dec) = {bin(byte)[2:].zfill(8)} (bin) -> '{char}'")
            if prev_byte is not None:
                diff = byte - prev_byte
                xor = byte ^ prev_byte
                print(f"  Δ from previous: {diff} steps")
                print(f"  XOR pattern: {bin(xor)[2:].zfill(8)}")
            prev_byte = byte

    return byte_data.decode('utf-8')

if __name__ == "__main__":
    # Example test vector
    test_bytes = [72, 101, 108, 108, 111]
    decoded = bytes_to_text(test_bytes)
    print(f"\nDecoded Text: {decoded}")