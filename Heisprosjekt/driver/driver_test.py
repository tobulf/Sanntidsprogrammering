from Driver import Elevator
from time import sleep


elev = Elevator()
elev.Queue[2] = True
elev.OpenDoor()

print elev.IsOrdersAbove(-10)

