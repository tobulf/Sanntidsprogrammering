from UDP_driver import UdpClient,UdpServer
from subprocess import call
import os
from Timer import Timer


Bcast ="129.241.187.255"

port = 20012

timer = Timer()
server = UdpClient((Bcast, port), "cunt")
server.imAliveMsg[1] = 0
client = UdpServer(port)





def main():
    count = 0
    client.ServerAddress = count
    client.Listen()
    if not client.connected:
        client.server.close()
        count = client.ServerAddress
        os.system("gnome-terminal -x -sh -c -python Oving6.py")
    while not client.connected:
        server.imAliveMsg[1] = count
        count+=1
        server.Heartbeat()
        timer.WaitNSeconds(1)

main()

