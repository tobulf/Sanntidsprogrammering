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
        # Internal Timer:
        self.timer = Timer()
        # Elevator current state, and previous state:
        self.currentstate = ElevatorState.Idle
        self.prevstate = ElevatorState.Idle
        # Initially the elevator is just IDLE in 1st floor:
        self.direction = MotorDirection.DirnStop
        # Initialize a internal queue with no orders:
        self.InternalQueue = [False] * Floors
        self.ExternalQueueDown = [False]*Floors # queue from external orders, determined by server
        self.ExternalQueueUp = [False] * Floors # queue from external orders, determined by server
        # Initialise the elevator, Makes it go to 1st floor:
        self.elev.set_motordirection(MotorDirection.DirnDown)
        while self.elev.get_floor_sensor_signal() == -1:
            pass
        self.elev.set_motordirection(MotorDirection.DirnStop)
        # Current floor
        self.currentfloor = self.elev.get_floor_sensor_signal()


    def Serve(self, TimeOut = 5):
        while True:
            # This is basicaly a state Machine for the elevator:
            if self.currentstate == ElevatorState.Running:
                # Using mutex to avoid Concurrency
                self.currentfloor = self.elev.get_floor_sensor_signal()
                try:
                    assert(self.currentfloor != -1)
                    # If the elevator gets to a floor it will stop the timer:
                    self.timer.StopTimer()
                    self.elev.set_floor_indicator(self.currentfloor)
                    #fix

                    if self.StopAtFloor():
                        # If it is a order at that floor, stop the elevator:
                        self.elev.set_motordirection(MotorDirection.DirnStop)
                        # Update states
                        self.prevstate = self.currentstate
                        self.currentstate = ElevatorState.Idle

                    elif self.StopAtFloor():
                        # If it is a order at that floor, stop the elevator:
                        self.elev.set_motordirection(MotorDirection.DirnStop)
                        # Update states
                        self.prevstate = self.currentstate
                        self.currentstate = ElevatorState.Idle
                except AssertionError:
                    # When the elevator is between floors, a timer is started, if the elevator does not reach a new floor within 5 seconds its considered stuck:
                    if not self.timer.started:
                        self.timer.StartTimer()
                    # If the elevator times out:
                    elif self.timer.GetCurrentTime() > TimeOut:
                        # elevator considers itself stuck and stops:
                        self.currentstate = ElevatorState.Error
                        self.elev.set_motordirection(MotorDirection.DirnStop)
                    pass

            elif self.currentstate == ElevatorState.Idle:
                # Checks the previous state
                if self.prevstate == ElevatorState.Running:
                    # If it was running, then it stopped due to an order at the current flor. Opens door.
                    self.OpenDoor()
                    # Turns of all the lights at the floor it arrived at:
                    KillLight(self.currentfloor, LampType.Command)
                    # Deletes the order from the Queue, assumes everyone enters/exits the elevator when the door open:
                    self.InternalQueue[self.currentfloor] = False
                    # mutex to prevent concurrency
                    mutex.acquire()
                    self.ExternalQueueDown[self.currentfloor] = False
                    self.ExternalQueueUp[self.currentfloor] = False
                    mutex.release()


                    # If there are orders above and the elevator was running it continues in that direction.
                    if self.IsOrdersAbove(self.currentfloor) and self.direction == MotorDirection.DirnUp:
                        self.elev.set_motordirection(MotorDirection.DirnUp)
                        self.currentstate = ElevatorState.Running
                        self.prevstate = ElevatorState.Idle

                    # If there are orders below and the elevator was running it continues in that direction.
                    elif self.IsOrdersBelow(self.currentfloor) and self.direction == MotorDirection.DirnDown:
                        self.elev.set_motordirection(MotorDirection.DirnDown)
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
                        # delete orders from Queues
                        self.ExternalQueueDown[self.currentfloor] = False
                        self.ExternalQueueUp[self.currentfloor] = False
                        self.InternalQueue[self.currentfloor] = False
                        # Open the door
                        self.OpenDoor()
                    # Checks if there are orders below the elevator and starts serving these if any.
                    elif self.IsOrdersAbove(self.currentfloor):
                        self.elev.set_motordirection(MotorDirection.DirnUp)
                        # Using mutex to avoid Concurrency
                        self.direction = MotorDirection.DirnUp
                        self.currentstate = ElevatorState.Running
                    # Checks if there are orders above the elevator and starts serving these if any.
                    elif self.IsOrdersBelow(self.currentfloor):
                        self.elev.set_motordirection(MotorDirection.DirnDown)
                        # Using mutex to avoid Concurrency
                        self.direction = MotorDirection.DirnDown
                        self.currentstate = ElevatorState.Running


            # Implement when the time comes... maybe never
            elif self.currentstate == ElevatorState.Obstruction:
                pass

            elif self.currentstate == ElevatorState.Error:
                while True:
                    print("Elevator stuck, Call maintenance...")
                    sleep(1)
            else:
                self.currentstate = ElevatorState.Error


    def OpenDoor(self):
        # Check that the elevator is not between floors:
        try:
            assert (self.elev.get_floor_sensor_signal() != -1)
            # Open the door:
            self.elev.set_door_open_lamp(1)
            # Standard hold time 3 seconds:
            sleep(3)
            # If Passenger holds the Command button, the elevator waits for a maximum of 10 more seconds:
            self.timer.StartTimer()
            while self.timer.GetCurrentTime() < 10 and self.elev.get_buttonsignal(LampType.Command, self.elev.get_floor_sensor_signal()):
                pass
            self.timer.StopTimer()
            # Close the door:
            self.elev.set_door_open_lamp(0)
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

