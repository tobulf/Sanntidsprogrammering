from Elev import elev
from time import sleep
from Timer import Timer
from LightCtrl import KillLight
from TypeClasses import*
from threading import Lock

mutex = Lock()

class Elevator(object):
    # when you initialise the class, you also initialise the elevator, goes to first floor.
    def __init__(self, Floors = 4):
        # Importing the driverClass:
        self.elev = elev
        # Number of floors:
        self.floors = Floors
        # Internal Timers, one for floor timeout, and one for timeouts between floors and one for the door:
        # Door:
        self.timer = Timer()
        # on Floor:
        self.floorTimer  = Timer()
        # between floors:
        self.runningTimer = Timer()
        # Elevator current state, and previous state:
        self.currentstate = ElevatorState.Idle
        self.prevstate = ElevatorState.Idle
        # Initially the elevator is just IDLE in 1st floor:
        self.direction = MotorDirection.DirnStop
        # Initialize a internal queue with no orders:
        self.InternalQueue = [False] * Floors
        self.ExternalQueueDown = [False]*Floors  # queue from external orders, determined by server
        self.ExternalQueueUp = [False] * Floors  # queue from external orders, determined by server
        # Initialise the elevator, Makes it go to 1st floor:
        self.elev.SetMotordirection(MotorDirection.DirnDown)
        while self.elev.GetFloorSensorSignal() == -1:
            pass
        self.elev.SetMotordirection(MotorDirection.DirnStop)
        self.OpenDoor()
        # Current floor
        self.currentfloor = self.elev.GetFloorSensorSignal()
        self.prevfloor    = self.currentfloor


    def Serve(self, TimeOut = 5):
        while True:
            # This is basicaly a state Machine for the elevator:
            if self.currentstate == ElevatorState.Running:
                # Using mutex to avoid Concurrency
                self.prevfloor    = self.currentfloor
                self.currentfloor = self.elev.GetFloorSensorSignal()
                try:
                    assert(self.currentfloor != -1)
                    # If the elevator gets to a floor it will stop the timer:
                    self.runningTimer.StopTimer()
                    self.elev.SetFloorIndicator(self.currentfloor)
                    #fix

                    if self.StopAtFloor():
                        # Stop the timer:
                        self.floorTimer.StopTimer()
                        # If it is a order at that floor, stop the elevator:
                        self.elev.SetMotordirection(MotorDirection.DirnStop)
                        # Update states
                        self.prevstate = self.currentstate
                        self.currentstate = ElevatorState.Idle

                    else:
                        # handles if the elevator is stuck at a floor:
                        if not self.floorTimer.started and self.prevfloor == self.currentfloor:
                            self.floorTimer.StartTimer()

                        elif self.prevfloor != self.currentfloor:
                            self.floorTimer.StopTimer()

                        elif self.floorTimer.GetCurrentTime() > 5:
                            self.currentstate = ElevatorState.Error
                            self.elev.SetMotordirection(MotorDirection.DirnStop)
                            self.direction = MotorDirection.DirnStop
                            self.floorTimer.StopTimer()

                except AssertionError:
                    # When the elevator is between floors, a timer is started, if the elevator does not reach a new floor within 5 seconds its considered stuck:
                    if not self.runningTimer.started:
                        self.runningTimer.StartTimer()
                    # If the elevator times out:
                    elif self.runningTimer.GetCurrentTime() > TimeOut:
                        # elevator considers itself stuck and stops:
                        self.currentstate = ElevatorState.Error
                        self.elev.SetMotordirection(MotorDirection.DirnStop)
                        self.direction = MotorDirection.DirnStop
                    pass

            elif self.currentstate == ElevatorState.Idle:
                # Checks the previous state
                if self.prevstate == ElevatorState.Running:
                    # Turns of the internal command-lights at the floor it arrived at:
                    KillLight(self.currentfloor, LampType.Command)
                    # If it was running, then it stopped due to an order at the current floor. Opens door.
                    self.OpenDoor()
                    # Deletes the order from the Queue, assumes everyone enters/exits the elevator when the door open:
                    # mutex to prevent concurrency
                    mutex.acquire()
                    self.InternalQueue[self.currentfloor] = False
                    self.ExternalQueueDown[self.currentfloor] = False
                    self.ExternalQueueUp[self.currentfloor] = False
                    mutex.release()


                    # If there are orders above and the elevator was running it continues in that direction.
                    if self.IsOrdersAbove(self.currentfloor) and self.direction == MotorDirection.DirnUp:
                        self.elev.SetMotordirection(MotorDirection.DirnUp)
                        self.currentstate = ElevatorState.Running
                        self.prevstate = ElevatorState.Idle

                    # If there are orders below and the elevator was running it continues in that direction.
                    elif self.IsOrdersBelow(self.currentfloor) and self.direction == MotorDirection.DirnDown:
                        self.elev.SetMotordirection(MotorDirection.DirnDown)
                        self.currentstate = ElevatorState.Running
                        self.prevstate = ElevatorState.Idle

                    # If there are no orders it just stays Idle:
                    else:
                        self.currentstate = ElevatorState.Idle
                        self.prevstate =  ElevatorState.Idle

                # If the elevator is IDLE or has served the floors in current direction it takes the first and best order.
                elif self.prevstate == ElevatorState.Idle:
                    # if the button is pressed when the lift is already on the floor:
                    if self.StopAtFloor():
                        # Kill all lights on the floor:
                        KillLight(self.currentfloor, LampType.Command)
                        # Using mutex to avoid Concurrency
                        mutex.acquire()
                        # delete orders from Queues
                        self.ExternalQueueDown[self.currentfloor] = False
                        self.ExternalQueueUp[self.currentfloor] = False
                        self.InternalQueue[self.currentfloor] = False
                        mutex.release()
                        # Open the door
                        self.OpenDoor()
                    # Checks if there are orders below the elevator and starts serving these if any.
                    elif self.IsOrdersAbove(self.currentfloor):
                        self.elev.SetMotordirection(MotorDirection.DirnUp)
                        # Using mutex to avoid Concurrency
                        self.direction = MotorDirection.DirnUp
                        self.currentstate = ElevatorState.Running
                    # Checks if there are orders above the elevator and starts serving these if any.
                    elif self.IsOrdersBelow(self.currentfloor):
                        self.elev.SetMotordirection(MotorDirection.DirnDown)
                        # Using mutex to avoid Concurrency
                        self.direction = MotorDirection.DirnDown
                        self.currentstate = ElevatorState.Running


            # Implement when the time comes... maybe never
            elif self.currentstate == ElevatorState.Obstruction:
                pass

            elif self.currentstate == ElevatorState.Error:
                # if the elevator is stuck at a floor, the door is kept open, if not it closes.
                while True:
                    try:
                        assert (self.elev.GetFloorSensorSignal() != -1)
                        self.elev.SetDoorOpenLamp(1)
                    except AssertionError:
                        self.elev.SetDoorOpenLamp(0)
                    print("Elevator stuck, Call maintenance...")

            else:
                self.currentstate = ElevatorState.Error


    def OpenDoor(self):
        # Check that the elevator is not between floors:
        try:
            assert (self.elev.GetFloorSensorSignal() != -1)
            # Open the door:
            self.elev.SetDoorOpenLamp(1)
            # Standard hold time 3 seconds:
            sleep(3)
            # If Passenger holds the Command button, the elevator waits for a maximum of 10 more seconds:
            self.timer.StartTimer()
            while self.timer.GetCurrentTime() < 10 and self.elev.GetButtonsignal(LampType.Command, self.elev.GetFloorSensorSignal()):
                pass
            self.timer.StopTimer()
            # Ensure that the light is turned of:
            KillLight(self.currentfloor, LampType.Command)
            # Close the door:
            self.elev.SetDoorOpenLamp(0)
        # If the elevator is between floors it does nothing:
        except AssertionError:
            pass



    def StopAtFloor(self):
        if self.InternalQueue[self.currentfloor] or (self.ExternalQueueDown[self.currentfloor] and self.direction == MotorDirection.DirnDown) or (self.ExternalQueueUp[self.currentfloor] and not self.IsOrdersBelow(self.currentfloor)):
            return True
        elif self.InternalQueue[self.currentfloor] or (self.ExternalQueueUp[self.currentfloor] and self.direction == MotorDirection.DirnUp) or (self.ExternalQueueDown[self.currentfloor] and not self.IsOrdersAbove(self.currentfloor)):
            return True

        else:
            return False


    def IsOrdersAbove(self, Floor):
        # Iterate over the floors above and check for orders:
        for i in range(Floor+1, self.floors):
            # Error handling in-case operator put in floors below 0
            try:
                # if there are any orders above pending in any queue
                if self.InternalQueue[i] or self.ExternalQueueDown[i] or self.ExternalQueueUp[i]:
                    return True
            except IndexError:
                pass
        return False

    def IsOrdersBelow(self, Floor):
        # Iterate over the Queue and check if there are orders below floor argument:
        for i in range(Floor-1, -1, -1):
            # Adding som error handling in-case operator put in too big floor
            try:
                # if there are any orders below pending in any queue
                if self.InternalQueue[i] or self.ExternalQueueDown[i] or self.ExternalQueueUp[i]:
                    return True
            except IndexError:
                pass
        return False

