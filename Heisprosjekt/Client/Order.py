from TypeClasses import*



class Order(object):
    def __init__(self, Floor = 4):
        # Just a list containing all orders from server:
        self.orderUp   = [False]*Floor
        self.orderDown = [False]*Floor

    def ExternalOrderServed(self, Floor, Direction):
        # Assert if there was an order served at that floor, returns it and deletes it:
        if Direction == Motor_direction.DIRN_UP:
            self.DeleteOrder(Floor, Direction)
            return [Floor, Direction]
        elif Direction == Motor_direction.DIRN_DOWN:
            self.DeleteOrder(Floor, Direction)
            return [Floor, Direction]
        else:
            return None

    def DeleteOrder(self, Floor, Direction):
        if Direction == Motor_direction.DIRN_UP:
            self.orderUp[Floor] = False
        elif Direction == Motor_direction.DIRN_DOWN:
            self.orderDown[Floor] = False

    def AppendOrder(self, Order):
        # Assert that there is an order to add:
        if Order:
            # Add order correctly
            if Order[1] == Motor_direction.DIRN_DOWN:
                self.orderDown[Order[0]] = True
            elif Order[0] == Motor_direction.DIRN_UP:
                self.orderUp[Order[0]] = True















