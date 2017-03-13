from TypeClasses import*
from ClientObject import Client


class Order(object):
    def __init__(self, Floor = 4):
        # Just a list containing all orders from server:
        self.orderUp   = [False]*Floor
        self.orderDown = [False]*Floor
        self.floors = Floor

    def ExternalOrderServed(self, Floor, Direction, State):
        # Assert if there was an order served at that floor, returns it and deletes it:
        if Direction == MotorDirection.DirnUp and self.orderUp[Floor]:
            self.DeleteOrder(Floor, Direction)
            return [Floor, Direction]

        elif Direction == MotorDirection.DirnDown and self.orderDown[Floor]:
            self.DeleteOrder(Floor, Direction)
            return [Floor, Direction]


        elif Direction == MotorDirection.DirnStop and (self.orderDown[Floor] or self.orderUp[Floor]):
            self.DeleteOrder(Floor, MotorDirection.DirnDown)
            self.DeleteOrder(Floor, MotorDirection.DirnUp)
            return [Floor, Direction]

        # Special if the elevator is on the top or bottom:
        elif Direction == MotorDirection.DirnDown and Floor == 0 and self.orderUp[Floor]:
            self.DeleteOrder(Floor, MotorDirection.DirnUp)
            return [Floor, MotorDirection.DirnUp]

        elif Direction == MotorDirection.DirnUp and Floor == (self.floors-1) and self.orderDown[Floor]:
            self.DeleteOrder(Floor, MotorDirection.DirnDown)
            return [Floor, MotorDirection.DirnDown]

        elif State == ElevatorState.Idle:
            if self.orderDown[Floor]:
                self.DeleteOrder(Floor, MotorDirection.DirnDown)
                return [Floor, MotorDirection.DirnDown]
            elif self.orderUp[Floor]:
                self.DeleteOrder(Floor, MotorDirection.DirnUp)
                return [Floor, MotorDirection.DirnUp]

        else:
            return None



    def DeleteOrder(self, Floor, Direction):
        if Direction == MotorDirection.DirnUp:
            self.orderUp[Floor] = False
        elif Direction == MotorDirection.DirnDown:
            self.orderDown[Floor] = False

    def AppendOrder(self, ClientObject):
        # Assert that there is an order to add:
        self.orderDown = ClientObject.orderDown
        self.orderUp = ClientObject.orderUp

