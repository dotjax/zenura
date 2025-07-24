def analyze(byte_list):
    result = []
    for b in byte_list:
        if 32 <= b <= 126:  # Printable ASCII range
            result.append(chr(b))
        else:
            result.append(f"[{b}]")  # Mark non-printable
    return result
