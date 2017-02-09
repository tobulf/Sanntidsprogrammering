from UDP_driver import UDP_SERVER
from time import sleep

port=(20010)



server=UDP_SERVER(port)

while True:
    server.listen()
    if (server.connected):
        print "connected to: ", server.serverAdress[0],server.serverAdress[1]
    elif not (server.connected):
    
        print "Currently Disconnected"
    sleep(1)
