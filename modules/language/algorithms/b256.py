elements = [0] * 256

def train(memory):
    byte_data = memory["analysis"]["byte"]
    for byte in byte_data:
        elements[byte] = min(elements[byte] + 1, 255)

def predict(byte_input):
    return sum(elements[b] for b in byte_input)