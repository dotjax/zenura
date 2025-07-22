from pprint import pformat

def write(result, path):
    with open(path, "w") as f:
        f.write("# Zenura Memory Snapshot\n")
        f.write("# Auto-generated neural imprint\n\n")
        f.write("transcode_result = ")
        f.write(pformat(result, indent=4, width=100))
        f.write("\n")