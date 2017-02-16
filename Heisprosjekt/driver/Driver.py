from Elev import Elev
from time import sleep

class Motor_direction:
    DIRN_DOWN = -1
    DIRN_STOP =  0
    DIRN_UP   =  1

class Lamp_type:
    BUTTON_CALL_UP   = 0
    BUTTON_CALL_DOWN = 1
    BUTTON_COMMAND   = 2



class Elevator(object):
    # when you initialise the class, you also initialise the elevator, goes 2 first floor.
    def __init__(self):
        self.elev = Elev()
        self.Queue = [4]
        # Initialise the elevator, Makes it go to 1st floor:
        self.elev.set_motordirection(Motor_direction.DIRN_DOWN)
        while self.elev.get_floor_sensor_signal() != 0:
            pass
        self.elev.set_motordirection(Motor_direction.DIRN_STOP)




















