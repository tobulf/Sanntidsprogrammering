from QueueMaster import QueueMaster
from TypeClasses import *
from Client import Client
from Costfunction import *
from random import randint
import json


Target = 1
queue1 = [True, True, True, True]
queue2 = [True, True, True, True]
queue3 = [True, False, True, True]
queue4 = [False, False, False, False]

client1 = Client(Address="123", Orderlist=queue1, Position=3, Direction= Motor_direction.DIRN_DOWN)
client2 = Client(Address="456", Orderlist=queue2, Position=3,Direction= Motor_direction.DIRN_DOWN)
client3 = Client(Address="678", Orderlist=queue3, Position=3,Direction= Motor_direction.DIRN_DOWN)
client4 = Client(Address="6789434", Orderlist=queue4, Position=3,Direction= Motor_direction.DIRN_DOWN)


Master = QueueMaster()
Master.AddClient(client1)
Master.AddClient(client2)
Master.AddClient(client3)
Master.AddClient(client4)

tel = {'ID':123, 'Serving':"123", 'Ligths':"456"}



