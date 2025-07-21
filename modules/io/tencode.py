def text_to_bytes(text=None, bits=8):
    if text is None:
        text = input("Enter text: ")
    # choose encoding width
    if bits == 8:
        raw = text.encode('utf-8')
        zfill_w = 8
    elif bits == 16:
        raw = text.encode('utf-16-be')
        zfill_w = 16
    else:
        raise ValueError("bits must be 8 or 16")

    # analysis buffer and return units
    # analysis of code units
    print("\nASCII Analysis:")
    prev_unit = None
    if bits == 8:
        units = list(raw)
    else:
        units = list(memoryview(raw).cast('H'))
    # iterate and print each unit
    for unit in units:
        char = chr(unit)
        print(f"{char}: {unit} (dec) = {bin(unit)[2:].zfill(zfill_w)} (bin)")
        if prev_unit is not None:
            diff = unit - prev_unit
            xorv = unit ^ prev_unit
            print(f"  Δ from {chr(prev_unit)}: {diff} steps")
            print(f"  XOR pattern: {bin(xorv)[2:].zfill(zfill_w)}")
        prev_unit = unit

    # return list of code units
    return units

if __name__ == "__main__":
    byte_output = text_to_bytes()
    print(f"\nRaw bytes: {bytes(byte_output)}")
    print(f"Byte values: {byte_output}")