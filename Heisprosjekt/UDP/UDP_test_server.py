from UDP_driver import UdpServer
import time
adress=("129.241.187.255",20010)
serverAdress=("120.23.40.5",230)

server=UdpServer(adress,serverAdress)

while True:
    server.Heartbeat()
    time.sleep(1)



