from Elev import elev
from time import sleep
from Timer import Timer
from LightCtrl import KillLights
from TypeClasses import *

class Elevator(object):
    # when you initialise the class, you also initialise the elevator, goes to first floor.
    def __init__(self, Floors = 4):
        self.elev = elev
        # Elevator current state, and previous state
        self.currentstate = Elevator_state.IDLE
        self.prevstate = Elevator_state.IDLE
        # Internal timer:
        self.timer = Timer()
        # Initially the elevator is just IDLE in 1st floor:
        self.direction = Motor_direction.DIRN_STOP
        # Initialize a internal queue with no orders:
        self.Queue = []
        for i in range(Floors):
            self.Queue.append(False)
        # Initialise the elevator, Makes it go to 1st floor:
        self.elev.set_motordirection(Motor_direction.DIRN_DOWN)
        while self.elev.get_floor_sensor_signal() != 0:
            pass
        self.elev.set_motordirection(Motor_direction.DIRN_STOP)
        # Current floor
        self.currentfloor = 0


    def Serve(self):
        while True:
            # This is basicaly a state Machine for the elevator:
            if self.currentstate == Elevator_state.RUNNING:
                self.currentfloor = self.elev.get_floor_sensor_signal()
                try:
                    assert(self.currentfloor != -1)
                    self.elev.set_floor_indicator(self.currentfloor)
                    if self.IsOrderAtFloor(self.currentfloor):
                        # If it is a order at that floor, stop the elevator:
                        self.elev.set_motordirection(Motor_direction.DIRN_STOP)
                        # Update states
                        self.prevstate = self.currentstate
                        self.currentstate = Elevator_state.IDLE
                except AssertionError:
                    pass

            elif self.currentstate == Elevator_state.IDLE:
                # Checks the previous state
                if self.prevstate == Elevator_state.RUNNING:
                    # If it was running, then it stopped due to an order at the current flor. Opens door.
                    self.OpenDoor()
                    # Turns of all the lights at the floor it arrived at:
                    KillLights(self.currentfloor)
                    # Deletes the order from the Queue:
                    self.Queue[self.currentfloor] = False
                    # If there are orders above and the elevator was running it continues in that direction.
                    if self.IsOrdersAbove(self.currentfloor) and self.direction == Motor_direction.DIRN_UP:
                        self.elev.set_motordirection(Motor_direction.DIRN_UP)
                        self.currentstate = Elevator_state.RUNNING
                        self.prevstate = Elevator_state.IDLE

                    # If there are orders below and the elevator was running it continues in that direction.
                    elif self.IsOrdersBelow(self.currentfloor) and self.direction == Motor_direction.DIRN_DOWN:
                        self.elev.set_motordirection(Motor_direction.DIRN_DOWN)
                        self.currentstate = Elevator_state.RUNNING
                        self.prevstate = Elevator_state.IDLE

                    # If there are no orders it just stays Idle:
                    else:
                        self.currentstate = Elevator_state.IDLE
                        self.prevstate =  Elevator_state.IDLE
                # If the elevator is IDLE or has served the floors in current direction it takes the first and best order.
                elif self.prevstate == Elevator_state.IDLE:
                    # Checks if there are orders below the elevator and starts serving these if any.
                    if self.IsOrdersAbove(self.currentfloor):
                        self.elev.set_motordirection(Motor_direction.DIRN_UP)
                        self.direction = Motor_direction.DIRN_UP
                        self.currentstate = Elevator_state.RUNNING
                    # Checks if there are orders above the elevator and starts serving these if any.
                    elif self.IsOrdersBelow(self.currentfloor):
                        self.elev.set_motordirection(Motor_direction.DIRN_DOWN)
                        self.direction = Motor_direction.DIRN_DOWN
                        self.currentstate = Elevator_state.RUNNING

            # Implement when the time comes... maybe never
            elif self.currentstate == Elevator_state.OBSTRUCTION:
                pass

            else:
                self.currentstate = Elevator_state.ERROR


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
            while self.timer.GetCurrentTime() < 10 and self.elev.get_buttonsignal(Lamp_type.BUTTON_COMMAND, self.elev.get_floor_sensor_signal()):
                pass
            self.timer.StopTimer()
            # Close the door:
            self.elev.set_door_open_lamp(0)
        # If the elevator is between floors it does nothing:
        except AssertionError:
            pass

    def IsOrderAtFloor(self, Floor):
        if self.Queue[Floor]:
            return True
        else:
            return False


    def IsOrdersAbove(self, Floor):
        # Iterate over the floors above and check for orders:
        for i in range(Floor+1, len(self.Queue)):
            # Error handling in-case operator put in floors below 0
            try:
                if self.Queue[i]:
                    return True
            except IndexError:
                pass
        return False

    def IsOrdersBelow(self, Floor):
        # Iterate over the Queue and check if there are orders below floor argument:
        for i in range(Floor-1, -1, -1):
            # Adding som error handling in-case operator put in too big floor
            try:
                if self.Queue[i]:
                    return True
            except IndexError:
                pass
        return False




























