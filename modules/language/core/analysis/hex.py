def analyze(byte_list):
    return [hex(b & 0xFFFF)[2:].zfill(4).upper() for b in byte_list]
