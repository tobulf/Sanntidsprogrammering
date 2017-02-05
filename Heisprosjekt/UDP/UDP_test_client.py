import UDP_driver
import time
port=(20020)



client=UDP_driver.UDP_CLIENT(port)

while True:
    client.listen()
    if (client.connected):
        print "connected to: ", client.serverAdress[0],client.serverAdress[1]
    elif not (client.connected):
    
    	print "Currently Disconnected"
    time.sleep(3)
