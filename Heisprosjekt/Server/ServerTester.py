from HTTPClient import HttpClient
from Client import Client
from time import sleep



IP    = "129.241.187.150"
Port  = 20010

path = "Test"
data = ""
object1 = Client(Address="1")
object2 = Client(Address="2")
object3 = Client(Address="3")
object4 = Client(Address="4")




client = HttpClient(IP, Port)
client.connected = True





