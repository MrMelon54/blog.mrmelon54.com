from glob import glob
from os.path import basename
from meta_reader import load_meta


def meta():
    return {
        "title": "Melon Blog",
        "author": "Melon",
        "og-title": "Melon Blog",
        "og-url": "https://blog.mrmelon54.com",
        "og-type": "object",
        "og-image": "https://blog.mrmelon54.com/logo.svg",
        "og-site_name": "blog.mrmelon54.com",
    }


def render(w):
    w.write("<header>\n")
    w.write(f"<h1>{meta()['title']}</h1>\n")
    w.write("</header>\n")
    w.write("<main>\n")
    w.write("<ul>\n")
    g = glob("post/*/*/*/*.page.html")
    g.sort(reverse=True)
    for i in g:
        with open(i, "r") as f:
            key = basename(i)[:-len(".page.html")]
            y = load_meta(f)
            ym = y["meta"]
            w.write(
                f"<li><a href=\"/post/{ym['post-date'].replace('-','/')}/{key}\">{ym['og-title']} - {ym['post-date']}</a></li>\n"
            )
    w.write("</ul>\n")
    w.write("</main>\n")
