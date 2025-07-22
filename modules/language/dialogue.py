from modules.language.algorithms import b256
from datetime import datetime

def train_on_live_input(memory):
    b256.train(memory)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"data/neural/language/learned/b256_neural_{timestamp}.py"
    with open(path, "w") as f:
        f.write(f"elements = {repr(b256.elements)}\n")
        