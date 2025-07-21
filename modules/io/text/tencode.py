def text_to_bytes(text=None):
    if text is None:
        text = input("Enter text: ")
    raw = text.encode('utf-8')
    zfill_w = 8

    print("Analysis:")
    prev_unit = None
    units = list(raw)
    for unit in units:
        char = chr(unit)
        print(f"{char}: {unit} (dec) = {bin(unit)[2:].zfill(zfill_w)} (bin)")
        if prev_unit is not None:
            diff = unit - prev_unit
            xorv = unit ^ prev_unit
            print(f"  Delta from {chr(prev_unit)}: {diff} steps")
            print(f"  XOR pattern: {bin(xorv)[2:].zfill(zfill_w)}")
        prev_unit = unit

    return units
