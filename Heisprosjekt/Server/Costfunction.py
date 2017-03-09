from TypeClasses import *
from time import sleep
# Insane COSTFUNCTION!

def FastestElevator(Clientlist, Externalorder):
    Clientindex = -1
    Length = -1
    for i in range(len(Clientlist)):
        temp = GetLength(Clientlist[i].orderUp, Clientlist[i].orderDown, Clientlist[i].internalOrders, Clientlist[i].direction, Externalorder, Clientlist[i].position)
        # Only considers Clients that is connected:
        if Length == -1 and Clientlist[i].connected:
            Length = temp
            Clientindex = i
        elif Length > temp and Clientlist[i].connected:
            Length = temp
            Clientindex = i
    return Clientindex


def GetLength(QueueUp, QueueDown, InternalQueue, Direction, Order, Currentposition):
    if Direction == Motor_direction.DIRN_DOWN and Order[0] < Currentposition:
        return LengthDownToTarget(Currentposition,QueueDown, Order[0])
    elif Direction == Motor_direction.DIRN_DOWN and Order[0] > Currentposition:
        return LengthUpToTarget(Currentposition, QueueUp, len(QueueUp)-1, EndTarget = True) + LengthDownToTarget(len(QueueUp)-1, QueueDown, Order[0])
    elif Direction == Motor_direction.DIRN_UP and Order[0] < Currentposition:
        return LengthUpToTarget(Currentposition, QueueUp, 0, EndTarget=True) + LengthDownToTarget(len(QueueDown), QueueDown, Order[0])
    elif Direction == Motor_direction.DIRN_UP  and Order[0] > Currentposition:
        return LengthUpToTarget(Currentposition, QueueUp, Order[0])


def LengthUpToTarget(Position, Queue, Target, EndTarget = False):
    # Count for number of orders in the queue
    orders = 0
    iterations = 0
    # Iterate over the Queue and check if there are orders below floor argument:
    for i in range(Position+1, len(Queue)):
        iterations = i
        # Error handling in-case operator put in floors below 0
        try:
            if i == Target and Queue[i] and EndTarget:
                orders += 2
                return orders + iterations - 1
            elif i == Target:
                return orders + iterations - 1
            elif Queue[i]:
                orders += 2
        except IndexError:
            # If we go out of index we return last:
            return orders + iterations
    return orders + iterations


def LengthDownToTarget(Position, Queue, Target, EndTarget = False):
    # Iterate over the Queue and check if there are orders below floor argument:
    orders = 0
    iterations = 0
    for i in range(Position-1, -1, -1):
        iterations += 1
        # Adding som error handling in-case operator put in too big floor
        try:
            if i == Target and Queue[i] and EndTarget:
                orders += 2
                return orders + iterations -1
            elif i == Target:
                return orders + iterations -1
            elif Queue[i]:
                orders += 2
        # If we go out of index we return last:
        except IndexError:
            return orders + iterations
    return orders + iterations

