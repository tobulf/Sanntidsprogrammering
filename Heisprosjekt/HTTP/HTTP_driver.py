from BaseHTTPServer import HTTPServer
from httplib import HTTPConnection
from json import dumps, loads


# Handler class should be in the network module, it does shit




class HttpClient(object):
    def __init__(self, address, port):
        self.address   = address
        self.port      = port
        self.client    = HTTPConnection(address, port)
        self.connected = false


    def PostRequest(self, path, message):
        assert(self.client.connect())
        data = dumps(message)
        self.client.request("POST", path, data)
        response = self.client.getresponse()
        # Check if the status is OK, Must add some kind of ERROR-handling here:
        if (response.status == 200):
            return loads(response.reason)


class HttpServer(object):
    def __init__(self, address, port, RequestHandler):
        self.address = (address, port)

        self.server  = HTTPServer(self.address, RequestHandler)
        self.serving = False

    def ServeOnce(self):
        if self.serving:
            self.server.handle_request()

    def Serve(self):
        while self.serving:
            self.server.handle_request()

    def ServeForever(self):
        self.server.serve_forever()


















