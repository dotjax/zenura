def analyze(byte_list):
    return [(byte_list[i] - byte_list[i - 1]) % 65536 for i in range(1, len(byte_list))]
