from QueueMaster import QueueMaster
import time
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

client1 = Client(Address="123", InternalOrders=queue1, Position=3, Direction= Motor_direction.DIRN_DOWN)
client2 = Client(Address="456", InternalOrders=queue2, Position=3, Direction= Motor_direction.DIRN_DOWN)
client3 = Client(Address="678", InternalOrders=queue3, Position=3, Direction= Motor_direction.DIRN_DOWN)
client4 = Client(Address="6789434", Order=[2, Motor_direction.DIRN_UP], Position = 3, Direction = Motor_direction.DIRN_DOWN)



Master = QueueMaster(Timeout=3)
Master.GetUpdate(client1)
Master.GetUpdate(client2)
Master.GetUpdate(client3)
client5 = Master.GotOrder(client4)
time.sleep(3)
print "slept"
Master.CheckTimeout()
print Master.clientlist[0].connected




