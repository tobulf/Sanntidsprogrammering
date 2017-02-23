from UDP_driver import UdpServer
from time import sleep

port=(20010)



server=UdpServer(port)

while True:
    server.Listen()
    if (server.connected):
        print "connected to: ", server.ServerAddress[0],server.ServerAddress[1]
    elif not (server.connected):
        print "Currently Disconnected"

