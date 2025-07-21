def bytes_to_text(byte_values, verbose=True):
    raw_bytes = bytes(byte_values)
    units = byte_values
    zfill_w = 8

    if verbose:
        print("Analysis:")
        prev_unit = None
        for unit in units:
            char = chr(unit)
            print(f"{unit} (dec) = {bin(unit)[2:].zfill(zfill_w)} (bin) -> '{char}'")
            if prev_unit is not None:
                diff = unit - prev_unit
                xorv = unit ^ prev_unit
                print(f"  Delta from previous: {diff} steps")
                print(f"  XOR pattern: {bin(xorv)[2:].zfill(zfill_w)}")
            prev_unit = unit

    return raw_bytes.decode('utf-8')
