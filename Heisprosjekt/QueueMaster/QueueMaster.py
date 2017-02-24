from Client import Client
from json import dumps, loads
from Timer import Timer
from Costfunction import PrioritizeOrder
from TypeClasses import *
from random import randint
from operator import add


#position = [floor, direction]

# Order = [floor, true/false]

class QueueMaster(object):
    def __init__(self):
        self.clientlist    = []
        self.timerlist     = []
        self.pendingorders = []
# Client-Server interfaces:
    def AddClient(self, Client):
        # If the client aint in the clientlist, it will be added:
        if not self.GetClientIndex(Client.address):
            # Adds the new client to the client list:
            self.clientlist.append(Client)
            # Each client has its own timer:
            self.timerlist.append(Timer())
            return True
        return False

    def GetUpdate(self, Client):
        # Tries to add the client in case its a new client, also returns just the Client, since it is new:
        if self.AddClient(Client):
            return Client
        # If the Client is in the list, it returns the latest Client object
        else:
            index = self.GetClientIndex(Client.address)
            self.UpdateData(Client)
            # If a order has been executed the order is updated:
            if Client.servestatus == Order_status.COMPLETE:
                self.clientlist[index].externalorders = Client.externalorders
            return self.clientlist[index]



    def GotOrder(self, Client):
        self.UpdateData(Client)
        index = self.GetClientIndex(Client)
        order = Client.order
        # The index is used to update the external Queue of the right client.
        priorityIndex = PrioritizeOrder(self.clientlist, order)

        self.clientlist[priorityIndex].externalorders[order] = True
        #Starts a timer to check if the given client serves the order.
        self.timerlist[priorityIndex].StartTimer()

        # Returns possibly updated object:
        return self.clientlist[index]



    # Internal Help-functions:

    def GetClientIndex(self, Clientaddress):
        # Internal function to find the Client in the clientlist.
        for i in range(len(self.clientlist)):
            if Clientaddress == self.clientlist[i].address:
                return i
        return False


    def UpdateData(self, Client):
        # Internal function to update non-vital data:
        index = self.GetClientIndex(Client)
        # Updates the orderList:
        self.clientlist[index].orderlist = Client.orderlist
        # Updates the position for the orderlist.
        self.clientlist[index].position = Client.position
        # Updates the direction:
        self.clientlist[index].direction = Client.direction

    def Timeout(self):
        # Internal function, Check all timers.
        for i in range(len(self.timerlist)):
            if self.timerlist[i].GetCurrentTime() > 60:
                return i
        return False



# Server to server interfaces:

    def toJson(self):
        #serialise clientlist:
        for i in range(len(self.clientlist)):
            temp = self.clientlist[i]
            self.clientlist[i] = temp.toJson()
        return dumps(self.__dict__)



    def fromJson(self, data):
        #deserializs clientlist
        dict = loads(data)
        self.clientlist = dict["clientlist"]
        for i in range(len(self.clientlist)):
            temp = self.clientlist[i]
            self.clientlist[i] = Client()
            self.clientlist[i].fromJson(temp)



















