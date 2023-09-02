from glob import glob
from datetime import datetime
from os.path import basename
import yaml

def meta():
  return {
    "title": "Melon Copy",
    "author": "Melon",
    "og-title": "Melon Copy",
    "og-url": "https://copy.mrmelon54.com",
    "og-type": "object",
    "og-image": "https://copy.mrmelon54.com/logo.svg",
    "og-site_name": "copy.mrmelon54.com",
  }

def render(writer):
  writer.write("<header>\n")
  writer.write(f"<h1>{meta()['title']}</h1>\n")
  writer.write("</header>\n")
  writer.write("<main>\n")
  writer.write("<ul>\n")
  g = glob("post/*/*/*/*.page")
  g.sort(reverse=True)
  for i in g:
    with open(i, 'r') as f:
      key = basename(i)[:-5]
      y = yaml.safe_load(f)
      ym = y['meta']
      writer.write(f"<li><a href=\"/post/{ym['post-date'].replace('-','/')}/{key}\">{ym['og-title']} - {ym['post-date']}</a></li>\n")
  writer.write("</ul>\n")
  writer.write("</main>\n")
