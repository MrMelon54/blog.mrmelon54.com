#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import io
from compile import compile_page, page_ext
import os.path


class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        p = self.path
        if p.startswith("/"):
            p = p[1:]

        if p == "":
            p = "index"

        for k in page_ext.keys():
            if os.path.exists("./" + p + k):
                with io.StringIO() as a:
                    if compile_page(a, "./" + p + k):
                        a.seek(0, 0)
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(a.read().encode("utf-8"))
                    else:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b"Failed to compile page")
                return

        self.path = "public/" + p
        SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8080), MyServer)
    print("Server started: http://localhost:8080")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
