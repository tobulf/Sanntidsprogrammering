from UDP_driver import UdpClient
import time
port=(20020)



client=UdpClient(port)

while True:
    client.Listen()
    if (client.connected):
        print "connected to: ", client.serverAdress[0],client.serverAdress[1]
    elif not (client.connected):
    
    	print "Currently Disconnected"
    time.sleep(3)
