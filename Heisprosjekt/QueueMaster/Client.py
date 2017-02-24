from json import dumps, loads


class Client(object):

    # Constructor:
    # Object can contain all information needed for any client, default everything is set to None.

    def __init__(self, Address = None, Direction = None, Order = None, Externalorders = None, Servestatus = None, OrderId = None, Orderlist = [None]*4, Position = None, Externallights = [None]*4):
        self.address = Address
        # Current direction of the elevator:
        self.direction = Direction
        # Order is a new external order to be executed
        self.order = Order
        # All external orders client currently is serving, N floors long:
        self.externalorders = Externalorders
        # Status of all external orders, list that is N floors long:
        self.servestatus = Servestatus
        # ID of the finished Order:
        self.orderid = OrderId
        # List of all current orders / all floors where elevator will stop:
        self.orderlist = Orderlist
        # Current position of the elevator:
        self.position = Position
        # List of external light orders:
        self.externallights = Externallights




    def toJson(self):
        return dumps(self.__dict__)

    def fromJson(self, Data):
        # Take in serialized object and construct a dict:
        self.dict = loads(Data)
        # Decompose the dict into the new object:
        self.address        = self.dict["address"]
        self.order          = self.dict["order"]
        self.direction      = self.dict["direction"]
        self.externalorders = self.dict["externalorders"]
        self.orderlist      = self.dict["orderlist"]
        self.position       = self.dict["position"]
        self.externallights = self.dict["externallights"]
        self.servestatus    = self.dict["servestatus"]
        self.orderid        = self.dict["orderid"]


