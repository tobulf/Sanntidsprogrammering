from ClientObject import Client
from json import dumps, loads
from Timer import Timer
from Costfunction import FastestElevator
from TypeClasses import *





# Order = [floor, LampType]
# Ordercomplete = [floor, Direction]

class QueueMaster(object):
    def __init__(self, Floors = 4, Timeout = 3):
        # Client list and timerlist for all clients:
        self.clientlist      = []
        self.timerlist       = []
        # Declare a LightList with all external lights initially zero:
        self.LightListUp   = [False]*Floors
        self.LightListDown = [False]*Floors
        # Variable for max amount of seconds a elevator can use on a Order:
        self.timeout = Timeout*Floors
        # Number of floors
        self.floors = Floors
        # Printing timer:
        self.printTimer = Timer()


# Client-Server interfaces:
    def GetUpdate(self, Client):
        # Tries to add the client in case its a new client, also returns just the Client, since it is new:
        self.AddClient(Client)
        # Find The index in clientlist:
        index = self.GetClientIndex(Client.address)
        # Update the data for the client:
        self.UpdateData(Client, index)
        if not self.clientlist[index].connected:
            # If the client was disconnected, the server takes over the all the external orders:
            self.clientlist[index].orderUp = Client.orderUp
            self.clientlist[index].orderDown = Client.orderDown
            self.Reprioritize(index)
        # If a order has been executed:
        if Client.orderCompleted:
            self.OrderCompleted(Client.orderCompleted, index)
        # If the client has a faulty state:
        if Client.currentState == ElevatorState.Error:
            self.Reprioritize(index)
        self.PrintClientlist(RefreshRate=1)
        # Reprioritize after newest state and info:
        #self.Reprioritize(index)
        # Update the ligthlist:
        self.clientlist[index].lightsUp = self.LightListUp
        self.clientlist[index].lightsDown = self.LightListDown
        return self.clientlist[index]


    def GotOrder(self, Client):
        # Tries to add client
        self.AddClient(Client)
        # Finds index:
        index = self.GetClientIndex(Client.address)
        # If the client was disconnected, the server takes over the external orders:
        if not self.clientlist[index].connected:
            # If the client was disconnected, the server takes over the external orders:
            self.clientlist[index].orderUp = Client.orderUp
            self.clientlist[index].orderDown = Client.orderDown
        # Updates data:
        self.UpdateData(Client, index)
        # Pass on the order:
        self.PrioritizeOrder(Client.order)
        # Update the ligthlist:
        self.clientlist[index].lightsUp   = self.LightListUp
        self.clientlist[index].lightsDown = self.LightListDown
        # Returns possibly updated object:
        print self.clientlist[index].address, index
        return self.clientlist[index]



    def PrioritizeOrder(self, Order):
        # The index is used to update the external Queue of the right client.
        priorityIndex = FastestElevator(self.clientlist, Order)
        # Adds the order to the Clients order List.
        self.clientlist[priorityIndex].order = Order
        if priorityIndex == -1:
            # If nothing can be prioritized it does nothing with the order. All elevators are either stuck or disconnected...
            pass
        elif Order[1] == LampType.CallDown:
            self.clientlist[priorityIndex].orderDown[Order[0]] = True
            self.LightListDown[Order[0]] = True
        elif Order[1] == LampType.CallUp:
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
            if self.clientlist[Index].orderUp[i]:
                order = [i, LampType.CallUp]
                self.PrioritizeOrder(order)
            if self.clientlist[Index].orderUp[i]:
                order = [i, LampType.CallDown]
                self.PrioritizeOrder(order)


    # Internal Help-functions:
    def AddClient(self, Client):
        # If the client is not in the clientlist, it will be added:
        index = self.GetClientIndex(Client.address)
        if index == -1:
            print "New Client Added: ", Client.address
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
        return -1


    def UpdateData(self, Client, index):
        # Internal function to update non-vital data:
        # Updates the orderList:
        self.clientlist[index].internalOrders = Client.internalOrders
        # Updates the position for the orderlist.
        self.clientlist[index].position = Client.position
        # Updates the direction:
        self.clientlist[index].direction = Client.direction
        # Update the state of the Elevator:
        self.clientlist[index].currentState = Client.currentState
        # Updates status:
        self.clientlist[index].connected = True


    def GotExternalOrders(self, Client):
        # Iterates trough the order lists and check if there are any orders:
        for i in range(self.floors):
            if Client.orderDown[i] or Client.orderUp[i]:
                return True
        return False


    def OrderCompleted(self, Order, Index):
        # Update the correct Ligthtlist and the Queue:
        self.PrintOrder(Order)
        # Delete the order for the Client
        self.clientlist[Index].order = None
        if Order[1] == MotorDirection.DirnDown:
            self.LightListDown[Order[0]] = False
            self.clientlist[Index].orderDown[Order[0]] = False
            # Stop the clients timer:
            self.timerlist[Index].StopTimer()
            if Order[0] == 0:
                # If the elevator is in the end, it should delete the oposite order.
                self.LightListUp[Order[0]] = False
                self.clientlist[Index].orderUp[Order[0]] = False
                # If the client has more orders start the timer again:
            if self.GotExternalOrders(self.clientlist[Index]):
                # Start timer
                self.timerlist[Index].StartTimer()

        elif Order[1] == MotorDirection.DirnUp:
            self.LightListUp[Order[0]] = False
            self.clientlist[Index].orderUp[Order[0]] = False
            # Stop the clients timer:
            self.timerlist[Index].StopTimer()
            #If the elevator is in the end, it should delete the oposite order.
            if Order[0] == self.floors-1:
                self.LightListDown[Order[0]] = False
                self.clientlist[Index].orderDown[Order[0]] = False
            # Check for more externalOrders:
            if self.GotExternalOrders(self.clientlist[Index]):
                # Start timer
                self.timerlist[Index].StartTimer()

        elif Order[1] == MotorDirection.DirnStop:
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
        # Make a temporary list to manipulate
        templist = []
        # declare a temporary Queuemaster object to manipulate:
        tempObj = QueueMaster()
        # serialise clientlist:
        for i in range(len(self.clientlist)):
            temp = self.clientlist[i].toJson()
            templist.append(temp)
        tempObj.clientlist = templist
        tempObj.LightListDown = self.LightListDown
        tempObj.LightListUp = self.LightListUp
        temp = tempObj.__dict__
        # Serialize every list and info, not the Timer list which is not serializable
        try:
            return dumps({'clientlist': temp['clientlist'], 'LightListUp': temp['LightListUp'], 'LightListDown': temp['LightListDown']})
        except TypeError:
            # If some issue occurs it just returns nothing.
            return dumps(None)


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
                # Adds a timer to all clients
                if len(self.timerlist) != len(self.clientlist):
                    # if there are not enough timers:
                    self.timerlist.append(Timer())
                # Starts all timers
                self.timerlist[i].StartTimer()
        except TypeError:
            pass




    # Print function for the clientlist:
    def PrintClientlist(self, RefreshRate=1):
        if self.printTimer.GetCurrentTime() > RefreshRate:
            # Print every second:
            self.printTimer.StartTimer()
            print "_______________________________________________"
            print "-------------Currently Serving:----------------"
            print "Client Address:".rjust(2), "Current Position:".rjust(4), "Current State:".rjust(6)
            for i in range(len(self.clientlist)):
                if self.clientlist[i].currentState == ElevatorState.Running:
                    print self.clientlist[i].address.rjust(0), repr(self.clientlist[i].position + 1).rjust(8), "Running".rjust(16)
                elif self.clientlist[i].currentState == ElevatorState.Idle:
                    print self.clientlist[i].address.rjust(0), repr(self.clientlist[i].position + 1).rjust(8), "Idle".rjust(16)
                elif self.clientlist[i].currentState == ElevatorState.Error:
                    print self.clientlist[i].address.rjust(0), repr(self.clientlist[i].position + 1).rjust(8), "Error".rjust(16)
        if not self.printTimer.started:
            self.printTimer.StartTimer()

    def PrintOrder(self, Order):
        print "A Order Has Been Completed!"
        print "___________________________"
        print "At Floor:".rjust(2), "Direction:".rjust(5)
        if Order[1] == MotorDirection.DirnDown:
            print repr(Order[0] + 1).rjust(8), "Up".rjust(10)
        elif Order[1] == MotorDirection.DirnUp:
            print repr(Order[0]+1).rjust(8), "Up".rjust(10)
        print "---------------------------"








