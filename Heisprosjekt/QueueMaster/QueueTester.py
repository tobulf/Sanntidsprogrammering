from QueueMaster import QueueMaster
from Client import Client

client1=Client(Address="123")
client2=Client(Address="456")
client3=Client(Address="678")

Master = QueueMaster()
Master.AddClient(client3)
Master.AddClient(client3)
Master.AddClient(client3)

print len(Master.clientlist)


