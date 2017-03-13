import socket
from json import dumps, loads
from Timer import Timer
from time import sleep



class UdpClient(object):
    def __init__(self, Bcast, IP, Port):
        self.timer = Timer()
        self.Address       = (Bcast, Port)
        self.Port          = Port
        self.ServingAdress = IP
        self.imAliveMsg    = ["im alive", self.ServingAdress]
        self.ServerAdress  = ""
        self.ServingServer = False
        self.client        = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set settings to broadcast:
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Set shared port:
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to Port
        self.client.bind(('', self.Port))
        # Set possibility to check buffer even if its nothing there
        self.client.setblocking(0)



    def Heartbeat(self):
        # function to send out heartbeat signal on UDP
        # serialize data with json, catch eventual error:
        try:
            data = dumps(self.imAliveMsg)
        except TypeError:
            pass
        try:
            # send im alive signal:
            self.client.sendto(data, (self.Address))
        except IOError as DC:
            # If the networkCable is pulled, we catch the error and set the server to Not serving.
            if DC.errno == 101:
                print "DISCONNECTED!"
                self.ServingServer = False
            pass


    def Listen(self, TimeOut=0.01):
        try:
            data = self.client.recv(1024)
            # if there is nothing in the buffer it throws an exception an passes.
            message = loads(data)
            if not message[0] == "im alive":
                if not self.timer.started:
                    self.timer.StartTimer()
                elif self.timer.GetCurrentTime() > TimeOut:
                    self.ServingServer = True
                    self.timer.StopTimer()

            elif message[0] == "im alive" and not self.ServingServer:
                # Store the other server address for backup:
                self.ServerAdress = message[1]
                self.ServingServer = False
                self.timer.StopTimer()
        except (socket.error,TypeError, ValueError):
            if not self.timer.started:
                    #starts the internal timer
                    self.timer.StartTimer()
            elif self.timer.GetCurrentTime() > TimeOut:
                #if It has gone more than Three seconds it considers itself as the serving server
                self.ServingServer = True
                # stop timer:
                self.timer.StopTimer()
            pass
