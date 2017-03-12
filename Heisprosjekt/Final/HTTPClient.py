import socket
from ClientObject import Client
from QueueMaster import QueueMaster
from httplib import *
from json import dumps, loads
from time import sleep



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
            except (socket.error, TypeError, BadStatusLine):
                self.connected = False
                return None
            
            
            
    def GetRequest(self, path=""):
        if self.connected:
            try:
                self.client.connect()
                # Send the request as a path
                self.client.request("GET", path)
                # wait for response:
                response = self.client.getresponse()
                # Check if the status is OK:
                if (response.status == 200):
                    self.connected = True
                    data = response.reason
                    backup = QueueMaster()
                    backup.fromJson(data)
                    if backup:
                        return backup
                    else:
                        return None
            except (socket.error, TypeError, BadStatusLine):
                self.connected = False

                return None

