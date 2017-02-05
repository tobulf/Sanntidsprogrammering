import UDP_driver
import time
adress=("129.241.187.255",20010)
serverAdress=("120.23.40.5",230)

server=UDP_driver.UDP_SERVER(adress,serverAdress)

while True:
    server.heartbeat()
    time.sleep(1)



