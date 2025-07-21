def bytes_to_text(byte_values, bits=8, verbose=True):
    # reconstruct raw buffer depending on bit-width
    if bits == 8:
        raw_bytes = bytes(byte_values)
        units = byte_values
        zfill_w = 8
    elif bits == 16:
        # each value is a 16-bit word
        ba = bytearray()
        for w in byte_values:
            ba.extend(w.to_bytes(2, 'big'))
        raw_bytes = bytes(ba)
        units = byte_values
        zfill_w = 16
    else:
        raise ValueError("bits must be 8 or 16")

    if verbose:
        print("\nASCII Analysis:")
        prev_unit = None
        for unit in units:
            char = chr(unit)
            print(f"{unit} (dec) = {bin(unit)[2:].zfill(zfill_w)} (bin) -> '{char}'")
            if prev_unit is not None:
                diff = unit - prev_unit
                xorv = unit ^ prev_unit
                print(f"  Δ from previous: {diff} steps")
                print(f"  XOR pattern: {bin(xorv)[2:].zfill(zfill_w)}")
            prev_unit = unit

    # decode from raw bytes using UTF encoding matching bit-width
    if bits == 8:
        return raw_bytes.decode('utf-8')
    else:
        return raw_bytes.decode('utf-16-be')

if __name__ == "__main__":
    # Example test vector
    test_bytes = [72, 101, 108, 108, 111]
    decoded = bytes_to_text(test_bytes)
    print(f"\nDecoded Text: {decoded}")