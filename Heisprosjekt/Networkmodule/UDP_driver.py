import socket
from json import dumps, loads

class UdpServer(object):
    def __init__(self,Port): # constructor, makes an socket named server.
        # Set up a UDP server:
        self.Address = ('',Port) # server own IP and PORT
        self.server  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server.bind(self.Address)
        # Set possibility to check buffer even if its nothing there
        self.server.setblocking(0)
        # variables to see if client is connected and to store serveradress.
        self.connected = False
        self.ServerAddress=("",0)


    def Listen(self):
        # function to listen on UDP for the client
        if self.connected:  # if it is connected, it checks the UDP message for "im alive" phrase.
            # try to check buffer and load json
            try:
                data = self.server.recv(1024)
            # if there is nothing in the buffer it throws an exception an passes.
                message = loads(data)
                if not message[0] == "im alive":
                    self.connected = False
            # Catches both socket error and JSON error:
            except (socket.error, TypeError, ValueError):
                self.connected = False
                pass

        if not self.connected: # if the client ain't connected it will read IP and PORT for the SERVER serving
            try:
                data = self.server.recv(1024)
                # error handling for Json encoding:
                message = loads(data)
                if message[0] == "im alive":
                    self.ServerAddress = message[1]
                    self.connected = True
            except (socket.error, TypeError, ValueError):
                pass




class UdpClient(object):
    def __init__(self, Adress, ServingAdress):
        self.Adress        = Adress
        self.ServingAdress = ServingAdress
        self.imAliveMsg    = ["im alive", ServingAdress]
        self.ServingServer = False
        self.client        = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # standard variables, im alive message and if the client is serving.


    def Heartbeat(self):
        # function to send out heartbeat signal on UDP
        # Set settings to broadcast:
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        # serialize data with json:
        try:
            data = dumps(self.imAliveMsg)
        except TypeError:
            data = "Error"
            pass
        # send im alive signal:
        self.client.sendto(data, (self.Adress))
