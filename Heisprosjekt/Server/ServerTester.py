
from Heisprosjekt.Server.Client import Client

from Sanntidsprogrammering.Heisprosjekt.Client.HTTPClient import HttpClient

IP    = "129.241.187.150"

from HTTPClient import HttpClient
from Client import Client
from json import dumps

IP    = "129.241.187.156"

Port  = 20010

path = "basst"
data = "data"
object1 = Client(Address="1")
object2 = Client(Address="2")
object3 = Client(Address="3")
object4 = Client(Address="4")




client = HttpClient(IP, Port)
client.connected = True
while True:
    print client.PostRequest(path, data)







