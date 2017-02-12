from UDP_driver import UdpClient
from time import sleep
adress=("",20010)
serverAdress=("120.23.40.5",230)

server=UdpClient(adress,serverAdress)

while True:
    print "imalive!"
    server.Heartbeat()
    sleep(1)



