#!/usr/bin/env python3
import io
import shutil
from os import makedirs
import os.path
from os.path import dirname, basename
import importlib, importlib.util
from meta_reader import load_meta


def main():
    if os.path.exists("build"):
        shutil.rmtree("build")
    shutil.copytree("public/", "build/")
    gen_pages()


def loader(p):
    spec = importlib.util.spec_from_file_location("", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render_static_page(w, input):
    with open(input, "r") as f:
        m = load_meta(f)
        f.seek(0, 0)
        gen_with_layout(w, m["meta"], f.read())


def render_dynamic_page(w, input):
    m = loader(input)
    with io.StringIO() as f:
        m.render(f)
        f.seek(0, 0)
        gen_with_layout(w, m.meta(), f.read())


page_ext = {".page.html": render_static_page, ".page.py": render_dynamic_page}


def gen_pages():
    for root, dirs, files in os.walk(".", topdown=True):
        exclude = [".git", ".github", "build", "public", "__pycache__"]
        dirs[:] = [d for d in dirs if d not in exclude]

        for f in files:
            f1 = os.path.join(root, f)
            d = dirname(f1)
            f2 = basename(f1)
            f3 = transfer_page_name(f2)
            if f3 == None:
                continue

            print(f"Generating {f} -> {f3}")

            if not os.path.exists(f"build/{d}"):
                makedirs(f"build/{d}")

            with open(f"build/{d}/{f3}", "w") as w:
                compile_page(w, f1)


def transfer_page_name(f):
    for k in page_ext.keys():
        if f.endswith(k):
            return f[: -len(k)] + ".html"
    return None


def compile_page(w, f):
    for k in page_ext.keys():
        if f.endswith(k):
            page_ext[k](w, f)
            return True
    return False


def gen_with_layout(w, head, page):
    with open("+layout.html") as layout:
        for line in layout.readlines():
            if line.strip() == "{{head}}":
                write_meta(w, head)
            elif line.strip() == "{{page}}":
                w.write(page)
            else:
                w.write(line)


def write_meta(w, meta):
    w.write(f"<title>{meta['title']}</title>\n")
    w.write(f"<meta name=\"author\" content=\"{meta['author']}\">\n")
    w.write(f"<meta property=\"og:title\" content=\"{meta['og-title']}\">\n")
    w.write(f"<meta property=\"og:url\" content=\"{meta['og-url']}\">\n")
    w.write(f"<meta property=\"og:type\" content=\"{meta['og-type']}\">\n")
    w.write(f"<meta property=\"og:image\" content=\"{meta['og-image']}\">\n")
    w.write(f"<meta property=\"og:site_name\" content=\"{meta['og-site_name']}\">\n")


if __name__ == "__main__":
    main()
