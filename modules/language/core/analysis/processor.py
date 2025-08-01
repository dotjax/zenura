from modules.language.core.analysis.tools import ascii, binary, byte, delta, hex, xor
from modules.language.core.analysis.metadata import length, source, timestamp

def process(text):
    byte_data = text.encode('utf-8')

    result = {
        "metadata": {
            "length": length.generate(text),
            "timestamp": timestamp.generate(text),
            "source": source.generate(text),
        },
        "analysis": {
            "ascii": ascii.analyze(byte_data),
            "binary": binary.analyze(byte_data),
            "byte": byte.analyze(byte_data),
            "delta": delta.analyze(byte_data),
            "hex": hex.analyze(byte_data),
            "xor": xor.analyze(byte_data),
        }
    }

    return result
