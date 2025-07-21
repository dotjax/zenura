import os
import importlib.util
from datetime import datetime
from modules.io.text.tdecode import bytes_to_text
from modules.language.record import render_language_class

class Engine:
    def __init__(self, input_dir="data/input", output_dir="data/output"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.records = self._load_records()

    def _load_records(self):
        records = []
        for fname in os.listdir(self.input_dir):
            if fname.endswith(".py"):
                path = os.path.join(self.input_dir, fname)
                spec = importlib.util.spec_from_file_location("record_module", path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "LanguageRecord"):
                    records.append(mod.LanguageRecord())
        return records

    def _compare_delta(self, d1, d2):
        if len(d1) != len(d2):
            return float("inf")
        return sum(abs(a - b) for a, b in zip(d1, d2))

    def _compare_xor(self, x1, x2):
        if len(x1) != len(x2):
            return 0.0
        return sum(1 for a, b in zip(x1, x2) if a == b) / len(x1)

    def _find_best_record(self, delta8, xor8):
        best_record = None
        best_score = float("inf")
        for record in self.records:
            delta_score = self._compare_delta(delta8, record.delta8)
            xor_score = self._compare_xor(xor8, record.xor8)
            if delta_score < best_score and xor_score >= 0.6:
                best_score = delta_score
                best_record = record
        return best_record

    def _mutate_delta(self, delta):
        return [(x + 1 if x % 2 == 0 else x - 1) for x in delta]

    def _construct_mutated_values(self, base_value, mutated_delta):
        values = [base_value]
        total = base_value
        for delta in mutated_delta:
            total += delta
            values.append(total)
        return values

    def generate(self, input_text, word_values, delta8, xor8):
        reference = self._find_best_record(delta8, xor8)
        decode_text = None

        if reference:
            response_text = f"Echo: {reference.text}"
            output_word_values = word_values
            output_delta8 = delta8
            output_xor8 = xor8
            decode_text = reference.text
        else:
            mutated_delta = self._mutate_delta(delta8)
            response_text = f"Mutation ∆={mutated_delta}"

            try:
                mutated_values = self._construct_mutated_values(word_values[0], mutated_delta)
                decode_text = bytes_to_text(mutated_values, verbose=False)
            except Exception:
                mutated_values = word_values
                decode_text = None

            output_word_values = mutated_values
            output_delta8 = mutated_delta
            output_xor8 = [format(output_word_values[i] ^ output_word_values[i - 1], "08b") for i in range(1, len(output_word_values))]

        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        safe_label = "".join(c if c.isalnum() else "_" for c in response_text)[:10]
        fname = f"{timestamp}_{safe_label or 'response'}.py"
        output_path = os.path.join(self.output_dir, fname)

        response_data = {
            "text": response_text,
            "created": timestamp,
            "word_values": output_word_values,
            "delta8": output_delta8,
            "xor8": output_xor8,
        }

        if decode_text is not None:
            response_data["decode"] = decode_text

        class_code = render_language_class("LanguageRecord", response_data)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(class_code)

        return decode_text or response_text