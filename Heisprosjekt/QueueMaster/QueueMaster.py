from Client import Client
from json import dumps, loads


#position = [floor, direction]

# Order = [floor, true/false]

class QueueMaster(object):
    def __init__(self):
        self.clientlist = []

# Client-Server interfaces:
    def AddClient(self, Client):
        if not Client in self.clientlist:
            self.clientlist.append(Client)

    def GetQueue(self, Client):
        pass

    def GotExternalorder(self, Client):
        pass


    def UpdatePosition(self, Client):
        pass







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



















