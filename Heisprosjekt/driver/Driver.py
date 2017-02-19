from Elev import Elev
from time import sleep
from Timer import Timer
class Motor_direction:
    DIRN_DOWN = -1
    DIRN_STOP =  0
    DIRN_UP   =  1

class Lamp_type:
    BUTTON_CALL_UP   = 0
    BUTTON_CALL_DOWN = 1
    BUTTON_COMMAND   = 2



class Elevator(object):
    # when you initialise the class, you also initialise the elevator, goes to first floor.
    def __init__(self, Floors = 4):
        self.elev = Elev()
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




























