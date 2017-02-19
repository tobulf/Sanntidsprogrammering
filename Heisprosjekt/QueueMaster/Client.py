from json import dumps, loads


class Client(object):

    # Constructor:
    # Object can contain all information needed for any client, default everything is set to None.

    def __init__(self, Externallights = None, Position = None , Externalorder = None, Order = None, Orderlist = None, Address = None, Dict = None):
        self.address = Address
        self.order = Order
        self.externalorder = Externalorder
        self.orderlist = Orderlist
        self.dict = Dict
        self.position = Position
        self.externallights = Externallights


    def toJson(self):
        return dumps(self.__dict__)

    def fromJson(self, Dict):
        self.struct = loads(Dict)
        self.address = self.struct["address"]
        self.order = self.struct["order"]
        self.externalorder = self.struct["externalorder"]
        self.orderlist = self.struct["orderlist"]
        self.dict = self.struct["dict"]
        self.position = self.struct["position"]
        self.externallights = self.struct["externallights"]



