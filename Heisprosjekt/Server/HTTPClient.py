import socket
from Client import Client
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
                    backup = QueueMaster()
                    if backup:
                        backup.fromJson(response.reason)
                    else:
                        return None
            except (socket.error, TypeError, BadStatusLine):
                self.connected = False
                return None

