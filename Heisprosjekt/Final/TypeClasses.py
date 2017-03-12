# Classes containing Elevator button types, sort of like typedef:
class Order_status:
    PENDING  = 10
    COMPLETE = 11


class Motor_direction:
    DIRN_DOWN = -1
    DIRN_STOP =  0
    DIRN_UP   =  1

class MotorDirection:
    DirnDown = -1
    DirnStop =  0
    DirnUp   =  1


class LampType:
    ButtonCallUp   = 0
    ButtonCallDown = 1
    ButtonCommand   = 2

class Elevator_state:
    ERROR       = -1
    RUNNING     = 1
    OBSTRUCTION = 2
    IDLE        = 3

class ServerState:
    Listening = 1
    Serving   = 2

class Button_type:
    BUTTON_CALL_UP   = 0
    BUTTON_CALL_DOWN = 1
    BUTTON_COMMAND   = 2
