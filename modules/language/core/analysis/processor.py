from modules.language.core.analysis import ascii, binary, byte, delta, hex, xor
from modules.language.core.analysis.metadata import length, source, timestamp

def process(text):
    # Encode using UTF-16 little endian (2 bytes per character)
    byte_data = text.encode('utf-16-le')

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
