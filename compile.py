#!/usr/bin/env python3
import shutil
import os
from glob import glob
import yaml
from os.path import dirname, basename
import importlib, importlib.util

def main():
  shutil.rmtree("build")
  shutil.copytree("public/","build/")
  gen_dynamic_pages()
  gen_static_pages()

def loader(p):
  spec = importlib.util.spec_from_file_location("", p)
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  return mod

def get_static_yaml(i):
  x = None
  with open(i, 'r') as fOld:
    x = yaml.safe_load(fOld)
  return x

def gen_pages(ext, prepare, meta, render):
  g = glob("**/*"+ext, recursive=True)
  for i in g:
    d = dirname(i)
    f2 = basename(i)
    f3 = f2[:-len(ext)] + ".html"
    print(f"Generating {i} -> {f3}")
    if not os.path.exists(f"build/{d}"):
      os.makedirs(f"build/{d}")
    with (
      open(f"build/{d}/{f3}", 'w') as fNow,
      open("+layout.html", 'r') as fLay,
    ):
      mod = prepare(i)
      copy_lines(fLay.readlines(), mod, meta, render, fNow)

def copy_lines(lines, y, meta, render, fNow):
  for line in lines:
    if line.strip() == "{{head}}":
      write_meta(fNow, meta(y))
    elif line.strip() == "{{page}}":
      render(y, fNow)
    else:
      fNow.write(line)

def gen_dynamic_pages():
  gen_pages(".page.py", loader, lambda y: y.meta(), lambda y, fNow: y.render(fNow))

def gen_static_pages():
  gen_pages(".page", get_static_yaml, lambda y: y['meta'], lambda y, fNow: fNow.write(y['content']))

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
