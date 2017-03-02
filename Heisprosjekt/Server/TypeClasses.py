# Classes containing Elevator button types, sort of like typedef:
class Order_status:
    PENDING  = 10
    COMPLETE = 11


class Motor_direction:
    DIRN_DOWN = -1
    DIRN_STOP =  0
    DIRN_UP   =  1

class Lamp_type:
    BUTTON_CALL_UP   = 0
    BUTTON_CALL_DOWN = 1
    BUTTON_COMMAND   = 2

class Elevator_state:
    ERROR       = -1
    RUNNING     = 1
    OBSTRUCTION = 2
    IDLE        = 3

class Button_type:
    BUTTON_CALL_UP   = 0
    BUTTON_CALL_DOWN = 1
    BUTTON_COMMAND   = 2
