import socket
from json import dumps, loads
from Timer import Timer

class UdpServer(object):
    def __init__(self,Port): # constructor, makes an socket named server.
        # Set up a UDP server:
        self.Address = ('',Port) # server own IP and PORT
        # Internal timer:
        self.timer = Timer()
        # Making a socketserver:
        self.server  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server.bind(self.Address)
        # Set possibility to check buffer even if its nothing there
        self.server.setblocking(0)
        # variables to see if client is connected and to store serveradress.
        self.connected = False
        self.ServerAddress = ""


    def Listen(self):
        # function to listen on UDP for the client
        if self.connected:  # if it is connected, it checks the UDP message for "im alive" phrase.
            # try to check buffer and load json
            try:
                data = self.server.recv(1024)
            # if there is nothing in the buffer it throws an exception an passes.
                message = loads(data)
                if not message[0] == "im alive":
                    if not self.timer.started:
                        # start the timer
                        self.timer.StartTimer()
                    elif self.timer.GetCurrentTime() > 3:
                        # If DC for 3 seconds:
                        self.connected = False

            # Catches both socket error and JSON error:
            except (socket.error, TypeError, ValueError):
                if not self.timer.started:
                    self.timer.StartTimer()
                elif self.timer.started and self.timer.GetCurrentTime() > 3:
                    self.timer.StopTimer()
                    self.connected = False
                pass

        if not self.connected: # if the client ain't connected it will read IP and PORT for the SERVER serving
            try:
                data = self.server.recv(1024)
                # error handling for Json encoding:
                message = loads(data)
                if message[0] == "im alive":
                    if self.timer.started:
                        # Stop the timer if its counting:
                        self.timer.StopTimer()
                    self.ServerAddress = message[1]
                    self.connected = True
            except (socket.error, TypeError, ValueError):
                if not self.timer.started:
                    self.timer.StartTimer()
                elif self.timer.GetCurrentTime() > 3:
                    self.timer.StopTimer()
                    self.connected = False



