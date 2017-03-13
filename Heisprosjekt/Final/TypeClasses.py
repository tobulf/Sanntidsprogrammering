

# Classes containing Elevator button types, sort of like typedef:

class MotorDirection:
    DirnDown = -1
    DirnStop =  0
    DirnUp   =  1


class LampType:
    CallUp   = 0
    CallDown = 1
    Command   = 2

class ElevatorState:
    Error       = -1
    Running     = 1
    Obstruction = 2
    Idle        = 3


class ButtonType:
    CallUp   = 0
    CallDown = 1
    Command  = 2

