import os
import sys
import threading
from datetime import datetime
from modules.language.core.autonomy import daemon
from modules.language.core.analysis import processor
from modules.language.core.memory import saving
from modules.language.core.algorithms.basic import delta

def main():
    daemon_thread = threading.Thread(target=daemon.run, daemon=True)
    daemon_thread.start()
    try:
        while True:
            print("Main thread is running. Press Ctrl+C to exit.")
            text = input("Enter text: ")
            result = processor.process(text)
            print(result)
            saving.write_input(result, "data/neural/language/input/user/")
            print("Saved to data/neural/language/input/user/")
            learned = delta.train (result)
            print(learned)
            saving.write_learned(learned, "data/neural/language/learned/delta")
            print("Saved to data/neural/language/learned/delta")
    except KeyboardInterrupt:
        print("\nExiting cleanly.")
        sys.exit(0)
if __name__ == "__main__":
    main()
