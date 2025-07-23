# import time
#def run():
#    print("Daemon activated. Listening to memory...")
#    while True:       
#        time.sleep(15)
#if __name__ == "__main__":
#    run()

import time, os, importlib.util
from modules.language.core.algorithms.layered import bdx

def run():
    print("Daemon activated. Listening to memory...")
    last = None
    while True:
        files = sorted([f for f in os.listdir("data/neural/language/input/user") if f.startswith("user_")], reverse=True)
        if files:
            latest = os.path.join("data/neural/language/input/user", files[0])
            if latest != last:
                last = latest
                spec = importlib.util.spec_from_file_location("m", latest)
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                bdx.train(m.transcode_result)
        time.sleep(5)

if __name__ == "__main__":
    run()
