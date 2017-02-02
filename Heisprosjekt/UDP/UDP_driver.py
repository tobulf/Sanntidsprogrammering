import socket
import demjson










class UDP_CLIENT(object):
    def __init__(self,IP,PORT): #constructor, makes an socket named client.
        self.adress=(IP,PORT)
        self.client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.connected = False
        self.serverAdress


    def listen(self):
        self.client.bind(self.adress)
        if self.connected:
            data=self.client.recv(1024)
            message=demjson.decode(data)
            if not (len(message)>3):
                self.connected=False

        if not self.connected:
            data=self.client.recv(1024)
            message















class UDP_SERVER(object):
    def __init__(self, IP, PORT):
        self.adress = (IP, PORT)

    def heartbeat:



    def isAlive:

