from QueueMaster import QueueMaster
from Client import Client
import json
client1=Client(Address="123")
client2=Client(Address="456")
client3=Client(Address="678")

Master = QueueMaster()
Master.AddClient(client1)
Master.AddClient(client2)
Master.AddClient(client3)

list1 = True
list2 = True
list3 = list1+list2

print list3


