def analyze(byte_list):
    return [hex(b)[2:].zfill(2) for b in byte_list]