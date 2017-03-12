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
        if Direction == Motor_direction.DIRN_UP and self.orderUp[Floor]:
            self.DeleteOrder(Floor, Direction)
            return [Floor, Direction]

        elif Direction == Motor_direction.DIRN_DOWN and self.orderDown[Floor]:
            self.DeleteOrder(Floor, Direction)
            return [Floor, Direction]


        elif Direction == Motor_direction.DIRN_STOP and (self.orderDown[Floor] or self.orderUp[Floor]):
            self.DeleteOrder(Floor, Motor_direction.DIRN_DOWN)
            self.DeleteOrder(Floor, Motor_direction.DIRN_UP)
            return [Floor, Direction]

        # Special if the elevator is on the top or bottom:
        elif Direction == Motor_direction.DIRN_DOWN and Floor == 0 and self.orderUp[Floor]:
            self.DeleteOrder(Floor, Motor_direction.DIRN_UP)
            return [Floor, Motor_direction.DIRN_UP]

        elif Direction == Motor_direction.DIRN_UP and Floor == (self.floors-1) and self.orderDown[Floor]:
            self.DeleteOrder(Floor, Motor_direction.DIRN_DOWN)
            return [Floor, Motor_direction.DIRN_DOWN]

        elif State == Elevator_state.IDLE:
            if self.orderDown[Floor]:
                self.DeleteOrder(Floor, Motor_direction.DIRN_DOWN)
                return [Floor, Motor_direction.DIRN_DOWN]
            elif self.orderUp[Floor]:
                self.DeleteOrder(Floor, Motor_direction.DIRN_UP)
                return [Floor, Motor_direction.DIRN_UP]

        else:
            return None



    def DeleteOrder(self, Floor, Direction):
        if Direction == Motor_direction.DIRN_UP:
            self.orderUp[Floor] = False
        elif Direction == Motor_direction.DIRN_DOWN:
            self.orderDown[Floor] = False

    def AppendOrder(self, Order, ClientObject):
        # Assert that there is an order to add:
        self.orderDown = ClientObject.orderDown
        self.orderUp = ClientObject.orderUp