import socket
from Client import Client
from httplib import HTTPConnection
from QueueMaster import QueueMaster
from json import loads




class HttpClient(object):
    def __init__(self, address, port):
        self.address   = address
        self.port      = port
        self.client    = HTTPConnection(address, port)
        # internal variable to check connection:
        self.connected = False

    def PostRequest(self, path, data):
        Clientobject = Client()
        if self.connected:
            # Error handler, handles if not connected and if json doesnt work
            # If there is an error only returns a list with one element which is zero.
            try:
                self.client.connect()
                # Post a request with the message as body:
                self.client.request("POST", path, data)
                # wait for response:
                response = self.client.getresponse()
                # Check if the status is OK:
                if response.status == 200:
                    self.connected = True
                    Clientobject.fromJson(response.reason)
                    return Clientobject
                else:
                    return None
            except (socket.error, TypeError):
                self.connected = False
                return None

    def GetRequest(self, path=""):
        try:
            self.client.connect()
            # Send the request as a path
            self.client.request("POST", path)
            # wait for response:
            response = self.client.getresponse()
            # Check if the status is OK:
            if (response.status == 200):
                self.connected = True
                backup = QueueMaster()
                backup.fromJson(response.msg)
                return backup
        except (socket.error, TypeError):
            self.connected = False
            pass
