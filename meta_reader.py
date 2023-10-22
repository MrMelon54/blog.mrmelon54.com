import yaml


def load_meta(r):
    if r.readline() != "<!--\n":
        return None

    # read document
    document = ""
    while True:
        l = r.readline()
        if l == "-->\n":
            break
        document += l

    return yaml.safe_load(document)
