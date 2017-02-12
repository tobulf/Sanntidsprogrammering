from BaseHTTPServer import HTTPServer
from httplib import HTTPConnection
from json import dumps, loads




class HttpClient(object):
    def __init__(self, address, port):
        self.address   = address
        self.port      = port
        self.client    = HTTPConnection(address, port)
        #internal variable to check connection:
        self.connected = False


    def PostRequest(self, path, message):
        if self.connected:
            self.client.connect()
            #JSON encode the message:
            data = dumps(message)
            #Post a request with the message as body:
            self.client.request("POST", path, data)
            #wait for response:
            response = self.client.getresponse()
            # Check if the status is OK, Must add some kind of ERROR-handling here:
            if (response.status == 200):
                return loads(response.reason)



class HttpServer(object):
    def __init__(self, address, port, RequestHandler):
        self.address = (address, port)
        self.server  = HTTPServer(self.address, RequestHandler)
        #Initially server is not serving:
        self.serving = False

    def ServeOnce(self):
        #serves only once when called
        if self.serving:
            self.server.handle_request()

    def Serve(self):
        #servest as long as it is set to serve:
        while self.serving:
            self.server.handle_request()

    def ServeForever(self):
        #serves forever:
        self.server.serve_forever()


















