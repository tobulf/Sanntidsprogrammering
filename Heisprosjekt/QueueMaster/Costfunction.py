from Client import Client
from TypeClasses import *

# Insane COSTFUNCTION!

def PrioritizeOrder(Clientlist, externalorder):
    Clientindex = -1
    Length = -1
    for i in range(len(Clientlist)):
        temp = GetLength(Clientlist[i].orderlist, Clientlist[i].direction, externalorder, Clientlist[i].position)
        if Length == -1:
            Length = temp
            Clientindex = i
        elif Length > temp:
            Length = temp
            Clientindex = i
    return Clientindex


def GetLength(Queue, Direction, Target, Currentposition):
        if Target < Currentposition and Direction == Motor_direction.DIRN_DOWN:
            #Return the total length down to the Target
            return LengthDownToTarget(Currentposition, Queue, Target)
        elif Target > Currentposition and Direction == Motor_direction.DIRN_DOWN:
            #Return the total length down to the Last order, then back up to the Target
            return LengthDownToTarget(Currentposition, Queue, 0, EndTarget=True) + LengthUpToTarget(0, Queue, Target)
        elif Target < Currentposition and Direction == Motor_direction.DIRN_UP:
            #Return the total length up to the Last order, then back down to the Target
            return LengthUpToTarget(Currentposition, Queue, len(Queue)-1, EndTarget=True) + LengthDownToTarget(len(Queue)-1, Queue, Target)
        elif Target > Currentposition and Direction == Motor_direction.DIRN_UP:
            #Return the total length up to the Target
            return LengthUpToTarget(Currentposition, Queue, Target)


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
                orders+=2
                return orders + iterations -1
            elif i == Target:
                return orders + iterations -1
            elif Queue[i]:
                orders += 2
        # If we go out of index we return last:
        except IndexError:
            return orders + iterations
    return orders + iterations

