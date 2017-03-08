from Client import Client



class Order(object):
    def __init__(self, Floor = 4):
        # Just a list containing all orders from server:
        self.orderList = [None]*Floor

    def ExternalOrderServed(self, Floor):
        return self.orders[Floor]

    def DeleteOrder(self, Floor):
        self.orderList[Floor] = False

    def AppendOrder(self, Floor):










