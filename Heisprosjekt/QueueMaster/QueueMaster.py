from Client import Client
from json import dumps, loads
from Timer import Timer
from operator import add


#position = [floor, direction]

# Order = [floor, true/false]

class QueueMaster(object):
    def __init__(self):
        self.clientlist = []
        self.timerlist = []
# Client-Server interfaces:
    def AddClient(self, Client):
        # If the client aint in the clientlist, it will be added:
        for i in range(len(self.clientlist)):
            if Client.address == self.clientlist[i].address:
                return False
        # Adds the new client to the client list:
        self.clientlist.append(Client)
        # Each client has a own timer:
        self.timerlist.append(Timer())
        return True

    def GetUpdate(self, Client):
        # Tries to add the client in case its a new client, also returns just the Client, since it is new:
        if self.AddClient(Client):
            return Client
        # If the Client is in the list, it returns the latest Client object
        else:
            for i in range(len(self.clientlist)):
                if Client.address == self.clientlist[i].address:
                    return self.clientlist[i]


    def GotOrder(self, Client):
        # Tries to add the client in case its a new client
        self.AddClient(Client)





    def UpdatePosition(self, Client):
        # Tries to add the client in case its a new client
        self.AddClient(Client)








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



















