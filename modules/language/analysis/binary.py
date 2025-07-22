def analyze(byte_list, width=8):
    return [bin(b)[2:].zfill(width) for b in byte_list]