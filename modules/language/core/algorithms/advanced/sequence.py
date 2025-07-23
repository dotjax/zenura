elements_forward = [0] * 65536  # For (a << 8 | b)
elements_backward = [0] * 65536  # For (b << 8 | a)

def train(memory):
    byte_data = memory["analysis"]["byte"]
    for i in range(1, len(byte_data)):
        a = byte_data[i - 1]
        b = byte_data[i]
        fwd = (a << 8) | b
        rev = (b << 8) | a
        elements_forward[fwd] = min(elements_forward[fwd] + 1, 65535)
        elements_backward[rev] = min(elements_backward[rev] + 1, 65535)

def predict_next(current_byte):
    base = current_byte << 8
    transitions = elements_forward[base : base + 256]
    return transitions.index(max(transitions))

def predict_prev(current_byte):
    base = current_byte << 8
    transitions = elements_backward[base : base + 256]
    return transitions.index(max(transitions))
