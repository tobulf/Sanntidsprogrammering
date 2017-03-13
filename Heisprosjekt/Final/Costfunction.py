from TypeClasses import *
from ClientObject import Client


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
    if Direction == MotorDirection.DirnDown and Order[0] < Currentposition:
        # Merge the internal and external queue to one Queue:
        NewQueueDown = MergeQueue(QueueDown, InternalQueue, len(QueueDown) - 1, MotorDirection.DirnDown)
        return LengthDownToTarget(Currentposition, NewQueueDown, Order[0])

    elif Direction == MotorDirection.DirnDown and Order[0] > Currentposition:
        # Merge the internal and external queue to one Queue:
        NewQueueUp = MergeQueue(QueueUp, InternalQueue, Currentposition, MotorDirection.DirnUp)
        NewQueueDown = MergeQueue(QueueDown, InternalQueue, len(QueueDown)-1, MotorDirection.DirnDown)
        return LengthUpToTarget(Currentposition, NewQueueUp, len(QueueUp)-1, EndTarget = True) + LengthDownToTarget(len(QueueUp)-1, NewQueueDown, Order[0])

    elif Direction == MotorDirection.DirnUp and Order[0] < Currentposition:
        # Merge the internal and external queue to one Queue:
        NewQueueUp = MergeQueue(QueueUp, InternalQueue, Currentposition, MotorDirection.DirnUp)
        NewQueueDown = MergeQueue(QueueDown, InternalQueue, len(QueueDown) - 1, MotorDirection.DirnDown)
        return LengthUpToTarget(Currentposition, NewQueueUp, 0, EndTarget=True) + LengthDownToTarget(len(QueueDown), NewQueueDown, Order[0])

    elif Direction == MotorDirection.DirnUp  and Order[0] > Currentposition:
        # Merge the internal and external queue to one Queue:
        NewQueueUp = MergeQueue(QueueUp, InternalQueue, Currentposition, MotorDirection.DirnUp)
        return LengthUpToTarget(Currentposition, NewQueueUp, Order[0])


def MergeQueue(ExternalQueue, InternalQueue, From, Dir):
    # Merges 2 queues together element-vise, From a position, in a Direction til the end of the list in that direction.
    if Dir == MotorDirection.DirnUp:
        # iterate from From to end of the queue:
        for i in range(From, len(ExternalQueue)):
            # Error handling to make Fault tolerant
            try:
                # Merge each element along the way:
                ExternalQueue[i] = InternalQueue[i] or ExternalQueue[i]
            except IndexError:
                return ExternalQueue
        return ExternalQueue
    elif Dir == MotorDirection.DirnDown:
        # Iterate from to 0
        for i in range(From, -1, -1):
            # Error handling to make Fault tolerant
            try:
                #make assertion to never go out of bounds:
                assert i >= 0
                # Merge each element along the way:
                ExternalQueue[i] = InternalQueue[i] or ExternalQueue[i]
            except AssertionError, IndexError:
                return ExternalQueue
        return ExternalQueue


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

