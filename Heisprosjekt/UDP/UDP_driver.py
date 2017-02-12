import socket
import json

class UdpServer(object):
    def __init__(self,PORT): #constructor, makes an socket named server.
        #Set up a UDP server:
        self.adress=('',PORT) #server own IP and PORT
        self.server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server.bind(self.adress)
        #variables to see if client is connected and to store serveradress.
        self.connected = False
        self.serverAdress=("",0)


    def Listen(self):       #function to listen on UDP for the client
        if self.connected:  #if it is connected, it checks the UDP message for "im alive" phrase.
            data=self.server.recv(1024)
            message=json.loads(data)
            if not (message[0] == "im alive"):
                self.connected = False

        if not self.connected: #if the client ain't connected it will read IP and PORT for the SERVER serving
            data=self.server.recv(1024)
            message=json.loads(data)
            if (message[0] == "im alive"):
                self.serverAdress=message[1]
                self.connected = True



class UdpClient(object):
    def __init__(self, adress, servingAdress):
        self.adress = adress
        self.servingAdress=servingAdress
        self.client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #standard variables, im alive message and if the client is serving.
        self.imAliveMsg=["im alive", servingAdress]
        self.servingServer=False

    def Heartbeat(self):  #function to send out heartbeat signal on UDP
        #Set settings to broadcast:
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        #serialize data with json:
        data=json.dumps(self.imAliveMsg)
        #send im alive signal:
        self.client.sendto(data, (self.adress))
