def analyze(byte_list):
    return [hex(b & 0xFF)[2:].zfill(2).upper() for b in byte_list]
