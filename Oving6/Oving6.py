from UDP_driver import UdpClient,UdpServer
import subprocess as sub
from time import sleep
from Timer import Timer


Bcast ="129.241.187.255"

port = 20013

timer = Timer()
server = UdpClient((Bcast, port), "cunt")
client = UdpServer(port)





def main():
    sleep(3)
    count = 0
    client.Listen()
    while client.connected:
        client.Listen()
        count = client.ServerAddress
        print count
        sleep(1)
    if not client.connected:
        client.server.close()
        count = client.ServerAddress
        #os.system("gnome-terminal", "-x", "-sh", "-c", "-python Oving6.py")
        sub.Popen(["gnome-terminal", "-x", "sh", "-c", "python Oving6.py"]);
    while not client.connected:
        print count
        server.Heartbeat(count)
        count+=1
        sleep(1)
main()

