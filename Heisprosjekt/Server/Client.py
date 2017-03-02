from json import dumps, loads


class Client(object):
    # Constructor:
    # Object can contain all information needed for any client, default everything is set to None.
    def __init__(self, Address = None, Direction = None, Order = None, OrderCompleted = None, OrderDown = None, OrderUp = None, InternalOrders = [None]*4, Position = None, LightsUp = [None]*4, LightsDown = [None]*4):
        self.address = Address
        # Current direction of the elevator:
        self.direction = Direction
        # Order is a new external order to be executed containing floor ->[0] and direction->[1]
        self.order = Order
        # If an external order is completed this contains a List floor ->[0] and direction->[1]
        self.orderCompleted = OrderCompleted
        # List of all orders down:
        self.orderDown   = OrderDown
        # List of all orders up:
        self.orderUp     = OrderUp
        # List of all current orders / all floors where elevator will stop:
        self.internalOrders = InternalOrders
        # Current position of the elevator:
        self.position = Position
        # List of external lights up:
        self.lightsUp   = LightsUp
        # List of external lights down:
        self.lightsDown = LightsDown
        # Internal variable for the server to check if it is connected:
        self.connected = True

    def toJson(self):
        return dumps(self.__dict__)

    def fromJson(self, Data):
        # Take in serialized object and construct a dict:
        self.dict = loads(Data)
        # Decompose the dict into the new object:
        self.address        = self.dict["address"]
        self.order          = self.dict["order"]
        self.orderCompleted = self.dict["orderCompleted"]
        self.direction      = self.dict["direction"]
        self.orderDown      = self.dict["orderDown"]
        self.orderUp        = self.dict["orderUp"]
        self.internalOrders = self.dict["internalOrders"]
        self.position       = self.dict["position"]
        self.lightsUp       = self.dict["lightsUp"]
        self.lightsDown     = self.dict["lightsDown"]






