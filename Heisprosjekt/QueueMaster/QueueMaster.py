from Client import Client
from json import dumps, loads
from Timer import Timer
from Costfunction import FastestElevator
from TypeClasses import *




# Order = [floor, true/false]

class QueueMaster(object):
    def __init__(self, Floors = 4, Timeout = 60):
        # Client list and timerlist for all clients:
        self.clientlist      = []
        self.timerlist       = []
        # Declare a LightList with all external lights initially zero:
        self.LightListUp   = [False]*Floors
        self.LightListDown = [False]*Floors
        # Variable for max amount of seconds a elevator can use on a Order:
        self.timeout = Timeout

# Client-Server interfaces:
    def GetUpdate(self, Client):
        # Tries to add the client in case its a new client, also returns just the Client, since it is new:
        if self.AddClient(Client):
            return Client
        # If the Client is in the list, it returns the latest Client object
        else:
            index = self.GetClientIndex(Client.address)
            self.UpdateData(Client, index)
            # If a order has been executed:
            if Client.orderCompleted:
                self.OrderCompleted(Client.orderCompleted, index)
            return self.clientlist[index]


    def GotOrder(self, Client):
        # Finds index:
        index = self.GetClientIndex(Client)
        # Updates data:
        self.UpdateData(Client, index)
        # Pass on the order:
        self.PrioritizeOrder(Client.order)
        # Returns possibly updated object:
        return self.clientlist[index]


    def CheckTimeout(self):
        # Internal function, Check all timers.
        for i in range(len(self.timerlist)):
            # If there is a timeOut it Re prioritizes the orders
            if self.timerlist[i].GetCurrentTime() > self.timeout:
                self.timerlist[i].StopTimer()
                # Considers Client disconnected:
                self.clientlist[i].connected = False
                # Re prioritize external orders of given Client
                self.Reprioritize(i)



    # when a timeout occurs it reprioritizes the Orders of the client that timed out
    def Reprioritize(self, Index):
        #Checks all floors for orders:
        for i in range(len(self.clientlist[Index].OrdersUp)):
            # Reprioritize Both orders UP and DOWN:
            if self.clientlist[Index].OrdersUp:
                order = [i, Motor_direction.DIRN_UP]
                self.PrioritizeOrder(order)
            if self.clientlist[Index].OrdersUp:
                order = [i, Motor_direction.DIRN_DOWN]
                self.PrioritizeOrder(order)


    # Internal Help-functions:
    def AddClient(self, Client):
        # If the client is not in the clientlist, it will be added:
        if not self.GetClientIndex(Client.address):
            # Adds the new client to the client list:
            self.clientlist.append(Client)
            # Each client has its own timer:
            self.timerlist.append(Timer())
            return True
        return False

    def GetClientIndex(self, Clientaddress):
        # Internal function to find the Client in the clientlist.
        for i in range(len(self.clientlist)):
            if Clientaddress == self.clientlist[i].address:
                return i
        return False


    def UpdateData(self, Client, index):
        # Internal function to update non-vital data:
        # Updates the orderList:
        self.clientlist[index].internalOrders = Client.internalOrders
        # Updates the position for the orderlist.
        self.clientlist[index].position = Client.position
        # Updates the direction:
        self.clientlist[index].direction = Client.direction
        # Updates status:
        self.clientlist[index].connected = True

    def GotExternalOrders(self, Client):
        # Iterates trough the order lists and check if there are any orders:
        for i in range(Client.orderDown):
            if Client.orderDown[i] or Client.orderUp[i]:
                return True
        return False

    def OrderCompleted(self, Order, Index):
        # Update the correct Ligthtlist and the Queue:
        if Order[1] == Motor_direction.DIRN_DOWN:
            self.LightListDown[Order[0]] = False
            self.clientlist[Index].OrderDown = False
            # Check for more external orders:
            if self.GotExternalOrders(self.clientlist[Index]):
                # Reset timer:
                self.timerlist[Index].StopTimer()
                self.timerlist[Index].StartTimer()
            else:
                # Stop the timer
                self.timerlist[Index].StopTimer()
        elif Order[1] == Motor_direction.DIRN_UP:
            self.LightListUp[Order[0]] = False
            self.clientlist[Index].OrderUp = False
            # Check for more externalOrders:
            if self.GotExternalOrders(self.clientlist[Index]):
                # Reset timer:
                self.timerlist[Index].StopTimer()
                self.timerlist[Index].StartTimer()
            else:
                # Stop the timer
                self.timerlist[Index].StopTimer()

    def PrioritizeOrder(self, Order):
        # The index is used to update the external Queue of the right client.
        priorityIndex = FastestElevator(self.clientlist, Order[0])
        self.clientlist[priorityIndex].newOrders = True
        if Order[1] == Motor_direction.DIRN_DOWN:
            self.clientlist[priorityIndex].orderDown[Order[0]] = True
            self.LightListDown[Order[0]] = True
        elif Order[1] == Motor_direction.DIRN_UP:
            self.clientlist[priorityIndex].orderUp[Order[0]] = True
            self.LightListUp = True
        # Starts a timer to check if the given client serves the order.
        self.timerlist[priorityIndex].StartTimer()


    def CheckTimeout(self):
        # Internal function, Check all timers.
        for i in range(len(self.timerlist)):
            if self.timerlist[i].GetCurrentTime() > self.timeout:
                # Considers Client disconnected:
                self.clientlist[i].connected = False
                # Returns index of the Client that has timed out.
                return i
        return False


# Server to server interfaces:

    def toJson(self):
        #serialise clientlist:
        for i in range(len(self.clientlist)):
            temp = self.clientlist[i]
            self.clientlist[i] = temp.toJson()
        temp = self.__dict__
        # Serialize every list and info, not the Timer list which is not serializable
        try:
            return dumps({'clientlist':temp["clientlist"], 'LightListUp':temp["LightListUp"], 'LightListDown':temp["LightListDown"]})
        except TypeError:
            # If some issue occurs it just returns nothing.
            return ""


    def fromJson(self, data):
        #deserializs clientlist
        try:
            dict = loads(data)
            self.clientlist = dict["clientlist"]
            self.LightListUp = dict["LightListUp"]
            self.LightListDown = dict["LightListDown"]
            for i in range(len(self.clientlist)):
                temp = self.clientlist[i]
                self.clientlist[i] = Client()
                self.clientlist[i].fromJson(temp)
        except TypeError:
            pass


















