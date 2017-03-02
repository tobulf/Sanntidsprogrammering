import socket
from httplib import HTTPConnection
from json import dumps, loads



class HttpClient(object):
    def __init__(self, address, port):
        self.address   = address
        self.port      = port
        self.client    = HTTPConnection(address, port)
        # internal variable to check connection:
        self.connected = False

    def PostRequest(self, path, message):
        if self.connected:
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
                if response.status == 200:
                    self.connected = True
                    return loads(response.reason)
                else:
                    return None
            except (socket.error, TypeError):
                self.connected = False
                return None

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
