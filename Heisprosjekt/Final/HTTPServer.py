from BaseHTTPServer import HTTPServer


class HttpServer(object):
    def __init__(self, address, port, RequestHandler):
        self.address = (address, port)
        self.server  = HTTPServer(self.address, RequestHandler)
        # Bool variable to break serve:
        self.serving = False


    def ServeOnce(self):
        # Serves only once when called
        self.server.handle_request()

    def Serve(self):
        # Serves as long as it is set to serve:
        while self.serving:
            self.server.handle_request()

    def ServeForever(self):
        # Serves forever:
        self.server.serve_forever()


















