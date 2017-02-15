



#position = [floor, direction]
# Order = [floor, true/false]



class QueueMaster(object):
    def __init__(self, Floors):
        self.clientlist      = []
        #list of Boolean values for orders:
        self.externalorders  = [Floors]
        # list of positions of all elevators
        self.elevatorpos     = []
        # List of all external lights also Boolean
        self.external_lights = [Floors]



# Client-Server interfaces:
    def AddClient(self, ClientAdress, Position):
        self.clientlist.append(ClientAdress)
        self.elevatorpos.append(Position)

    def GetQueue(self, ClientAdress, Position):


    def GotExternalorder(self, Order):
        #Updates the order in the directory:
        try:
            self.externalorders[Order[0]] = Order[1]
        except IndexError:
            pass

    def UpdatePosition(self, ClientAdress, Postition):







# Server to server interfaces:

    def GetAllOrders(self):
        return [self.clientlist, self.externalorders, self. elevatorpos, self.external_lights]

    def BackUp(self, AllOrders):
        self.clientlist      = AllOrders[0]
        self.externalorders  = AllOrders[1]
        self. elevatorpos    = AllOrders[2]
        self.external_lights = AllOrders[3]


















