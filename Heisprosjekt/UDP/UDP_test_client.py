import UDP_driver
import time
adress=("129.241.187.255",20010)



client=UDP_driver.UDP_CLIENT(adress)

while True:
    client.listen()
    if (client.connected):
        print "connected to: ", client.serverAdress[0],client.serverAdress[1]
    if not (client.connected):
        print "Currently disconected: "
    time.sleep(3)