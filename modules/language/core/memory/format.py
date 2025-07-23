def write(result, path):
    with open(path, "w") as f:
        f.write("# Auto-generated neural imprint\n")
        f.write("transcode_result = ")
        f.write(repr(result))