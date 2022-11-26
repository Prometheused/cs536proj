import SimpleHTTPServer
import SocketServer
import urlparse

class CustomResponseHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("a" * 9000)
        self.wfile.close()

httpd = SocketServer.TCPServer(("", 80), CustomResponseHandler)
httpd.serve_forever()
