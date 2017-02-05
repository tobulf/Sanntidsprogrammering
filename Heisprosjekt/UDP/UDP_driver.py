import socket
import json

class UDP_CLIENT(object):
    def __init__(self,PORT): #constructor, makes an socket named client.
        #Set up a UDP client:
        self.adress=('',PORT) #Clients own IP and PORT
        self.client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.client.bind(self.adress)
        #variables to see if client is connected and to store serveradress.
        self.connected = False
        self.serverAdress=("",0)


    def listen(self):       #function to listen on UDP for the client
        if self.connected:  #if it is connected, it checks the UDP message for "im alive" phrase.
            data=self.client.recv(1024)
            message=json.loads(data)
            if not (message[0] == "im alive"):
                self.connected = False

        if not self.connected: #if the client ain't connected it will read IP and PORT for the SERVER serving
            data=self.client.recv(1024)
            message=json.loads(data)
            if (message[0] == "im alive"):
                self.serverAdress=message[1]
                self.connected = True



class UDP_SERVER(object):
    def __init__(self, adress, servingAdress):
        self.adress = adress
        self.servingAdress=servingAdress
        self.server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #standard variables, im alive message and if the server is serving.
        self.imAliveMsg=["im alive", servingAdress]
        self.servingServer=False

    def heartbeat(self):  #function to send out heartbeat signal on UDP
        #Set settings to broadcast:
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        #serialize data with json:
        data=json.dumps(self.imAliveMsg)
        #send im alive signal:
        self.server.sendto(data, (self.adress))
