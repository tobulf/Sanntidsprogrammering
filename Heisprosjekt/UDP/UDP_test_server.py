from UDP_driver import UDP_CLIENT
from time import sleep
adress=("129.241.187.255",20010)
serverAdress=("120.23.40.5",230)

server=UDP_CLIENT(adress,serverAdress)

while True:
    print "imalive!"
    client.heartbeat()
    sleep(1)



