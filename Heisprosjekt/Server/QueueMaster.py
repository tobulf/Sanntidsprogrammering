from Client import Client
from json import dumps, loads
from Timer import Timer
from Costfunction import FastestElevator
from TypeClasses import *




# Order = [floor, LampType]
# Ordercomplete = [floor, Direction]

class QueueMaster(object):
    def __init__(self, Floors = 4, Timeout = 99999999):
        # Client list and timerlist for all clients:
        self.clientlist      = []
        self.timerlist       = []
        # Declare a LightList with all external lights initially zero:
        self.LightListUp   = [False]*Floors
        self.LightListDown = [False]*Floors
        # Variable for max amount of seconds a elevator can use on a Order:
        self.timeout = Timeout
        # Number of floors
        self.floors = Floors

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
            print Client.orderCompleted
            if Client.orderCompleted:
                self.OrderCompleted(Client.orderCompleted, index)
            # Update the ligthlist:
            print dumps(self.LightListUp), dumps(self.LightListDown)
            print dumps(self.clientlist[index].orderUp), dumps(self.clientlist[index].orderDown)
            self.clientlist[index].lightsUp = self.LightListUp
            self.clientlist[index].lightsDown = self.LightListDown
            return self.clientlist[index]


    def GotOrder(self, Client):
        # Tries to add client
        self.AddClient(Client)
        # Finds index:
        index = self.GetClientIndex(Client.address)
        # Updates data:
        self.UpdateData(Client, index)
        # Pass on the order:
        self.PrioritizeOrder(Client.order)
        # Update the ligthlist:
        print dumps(self.LightListUp), dumps(self.clientlist[index].orderUp)
        self.clientlist[index].lightsUp = self.LightListUp
        self.clientlist[index].lightsDown = self.LightListDown
        # Returns possibly updated object:
        return self.clientlist[index]



    def PrioritizeOrder(self, Order):
        # The index is used to update the external Queue of the right client.
        priorityIndex = FastestElevator(self.clientlist, Order[0])
        # Adds the order to the Clients order List.
        self.clientlist[priorityIndex].order = Order

        if Order[1] == LampType.ButtonCallDown:
            self.clientlist[priorityIndex].orderDown[Order[0]] = True
            self.LightListDown[Order[0]] = True
        elif Order[1] == LampType.ButtonCallUp:
            self.clientlist[priorityIndex].orderUp[Order[0]] = True
            self.LightListUp[Order[0]] = True
        # Starts a timer to check if the given client serves the order.
        self.timerlist[priorityIndex].StartTimer()


    def CheckTimeout(self):
        # Internal function, Check all timers.
        for i in range(len(self.timerlist)):
            # If there is a timeOut it Re prioritizes the orders
            if self.timerlist[i].GetCurrentTime() > self.timeout:
                self.timerlist[i].StopTimer()
                # Considers Client disconnected:
                self.clientlist[i].connected = False
                # Prints a message that an elevator has timed out:
                print "TIMEOUT!!"
                # Re prioritize external orders of given Client
                self.Reprioritize(i)




    # when a timeout occurs it reprioritizes the Orders of the client that timed out
    def Reprioritize(self, Index):
        #Checks all floors for orders:
        for i in range(self.floors):
            # Reprioritize Both orders UP and DOWN:
            if self.clientlist[Index].orderUp:
                order = [i, LampType.ButtonCallUp]
                self.PrioritizeOrder(order)
            if self.clientlist[Index].orderUp:
                order = [i, LampType.ButtonCallDown]
                self.PrioritizeOrder(order)


    # Internal Help-functions:
    def AddClient(self, Client):
        # If the client is not in the clientlist, it will be added:
        index = self.GetClientIndex(Client.address)
        if not index and len(self.clientlist) < 1:
            #rint "New Client Added: ", Client.address
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
        print "A ORDER IS COMPLETED!"
        # Delete the order for the Client
        self.clientlist[Index].order = None
        if Order[1] == Motor_direction.DIRN_DOWN:
            self.LightListDown[Order[0]] = False
            self.clientlist[Index].orderDown[Order[0]] = False
            if Order[0] == 0:
                # If the elevator is in the end, it should delete the oposite order.
                self.LightListUp[Order[0]] = False
                self.clientlist[Index].orderUp[Order[0]] = False
            # Check for more external orders:
            if self.GotExternalOrders(self.clientlist[Index]):
                # Reset timer:
                self.timerlist[Index].StartTimer()
            else:
                # Stop the timer
                self.timerlist[Index].StopTimer()
        elif Order[1] == Motor_direction.DIRN_UP:
            self.LightListUp[Order[0]] = False
            self.clientlist[Index].orderUp[Order[0]] = False
            #If the elevator is in the end, it should delete the oposite order.
            if Order[0] == self.floors-1:
                self.LightListDown[Order[0]] = False
                self.clientlist[Index].orderDown[Order[0]] = False
            # Check for more externalOrders:
            if self.GotExternalOrders(self.clientlist[Index]):
                # Reset timer:
                self.timerlist[Index].StartTimer()
            else:
                # Stop the timer
                self.timerlist[Index].StopTimer()

        elif Order[1] == Motor_direction.DIRN_STOP:
            self.LightListUp[Order[0]] = False
            self.LightListDown[Order[0]] = False
            self.clientlist[Index].orderUp[Order[0]] = False
            self.clientlist[Index].orderDown[Order[0]] = False
            # Check for more externalOrders:
            if self.GotExternalOrders(self.clientlist[Index]):
                # Reset timer:
                self.timerlist[Index].StartTimer()
            else:
                # Stop the timer
                self.timerlist[Index].StopTimer()



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


















