from BaseHTTPServer import HTTPServer
import socket
from httplib import HTTPConnection
from json import dumps, loads

from client import client


# kk

class HttpClient(object):
    def __init__(self, address, port):
        self.address   = address
        self.port      = port
        self.client    = HTTPConnection(address, port)
        # internal variable to check connection:
        self.connected = False

    def PostRequest(self, path, message):
        if self.connected:
            received = [0]
            # Error handler, handles if not connected and if json doesnt work
            # If there is an error only returns a list with one element which is zero.
            try:
                self.client.connect()
                # JSON encode the message:
                data = dumps(message)
                # Post a request with the message as body:
                self.client.request("POST", path, data)
                # wait for response:
                response = self.client.getresponse()
                # Check if the status is OK:
                if (response.status == 200):
                    received = loads(response.reason)
                    self.connected = True
            except (socket.error, TypeError):
                self.connected = False
                pass
            return received

    def GetRequest(self, path):
        try:
            self.client.connect()
            # Send the request as a path
            self.client.request("POST", path)
            # wait for response:
            response = self.client.getresponse()
            # Check if the status is OK:
            if (response.status == 200):
                self.connected = True
        except (socket.error, TypeError):
            self.connected = False
            pass


class HttpServer(object):
    def __init__(self, address, port, RequestHandler):
        self.address = (address, port)
        self.server  = HTTPServer(self.address, RequestHandler)
        # Initially server is not serving:
        self.serving = False

    def ServeOnce(self):
        # Serves only once when called
        if self.serving:
            self.server.handle_request()

    def Serve(self):
        # Serves as long as it is set to serve:
        while self.serving:
            self.server.handle_request()

    def ServeForever(self):
        # Serves forever:
        self.server.serve_forever()


















