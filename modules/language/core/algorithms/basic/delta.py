elements = [0] * 256  # 8-bit space

def train(memory):
    delta_values = memory["analysis"]["delta"]
    for val in delta_values:
        index = val % 256  # Wrap into 8-bit space
        elements[index] = min(elements[index] + 1, 255)
    return elements

def predict(byte_input):
    delta_pattern = [(byte_input[i] - byte_input[i - 1]) % 256 for i in range(1, len(byte_input))]
    return sum(elements[d] for d in delta_pattern)
