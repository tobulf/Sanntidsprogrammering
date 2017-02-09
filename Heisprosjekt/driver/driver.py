from Channels import Input,Output
from IO import IO

#0 means that it is undefined..


class Motor_speed:
    SPEED     = 2800

class Motor_direction:
    DIRN_DOWN = -1
    DIRN_STOP =  0
    DIRN_UP   =  1

class Lamp_type:
    BUTTON_CALL_UP   = 0
    BUTTON_CALL_DOWN = 1
    BUTTON_COMMAND   = 2



class Driver(object):
    def __init__(self):
        self.io=IO()
        for f in range(Input.N_FLOORS-1):
            for b in range(Input.N_FLOORS-1):
                self.set_button_lamp(b, f, 0)
        self.set_stop_lamp(0)
        self.set_door_open_lamp(0)
        self.set_floor_indicator(0)





    def set_motordirection(self, dirn):
        if dirn == Motor_direction.DIRN_STOP:
            self.io.IO_write_analog(Output.MOTOR)

        elif dirn > Motor_direction.DIRN_STOP:
            self.io.IO_clearBit(Output.MOTORDIR)
            self.io.IO_write_analog(Output.Motor, Motor_speed.SPEED)

        elif dirn < Motor_direction.DIRN_STOP:
            self.io.IO_setBit(Output.MOTORDIR)
            self.io.IO_write_analog(Output.MOTOR, Motor_speed.SPEED)





    def set_button_lamp(self, button, floor, value):
        assert floor  >= 0
        assert floor  <  Input.N_FLOORS
        assert button >= 0
        assert button <  Input.N_FLOORS
        if value:
            self.io.IO_setBit(Output.LAMP_MATRIX[floor][button])

        else:
            self.io.IO_clearBit(Output.LAMP_MATRIX[floor][button])



    def set_floor_indicator(self, floor):
        assert floor >= 0
        assert floor <  Input.N_FLOORS
        #Binary encoding, a light must always be on.
        if floor & 0x02:
            self.io.IO_setBit(Output.LIGHT_FLOOR_IND1)
        else:
            self.io.IO_clearBit(Output.LIGHT_FLOOR_IND1)

        if floor & 0x01:
            self.io.IO_setBit(Output.LIGHT_FLOOR_IND2)
        else:
            self.io.IO_clearBit(Output.LIGHT_FLOOR_IND2)



    def set_door_open_lamp(self, value):
        if value:
            self.io.IO_setBit(Output.LIGHT_DOOR_OPEN)
        else:
            self.io.IO_clearBit(Output.LIGHT_DOOR_OPEN)

    def set_stop_lamp(self, value):
        if value:
            self.io.IO_setBit(Output.LIGHT_STOP)
        else:
            self.io.IO_clearBit(Output.LIGHT_STOP)

    def get_buttonsignal(self, button, floor):
        assert floor  >= 0
        assert floor  < Input.N_FLOORS
        assert button >= 0
        assert button < Input.N_BUTTONS
        return self.io.IO_readBit(Input.BUTTON_MATRIX[floor][button])

    def get_floor_sensor_signal(self):
        if self.io.IO_readBit(Input.SENSOR_FLOOR1):
            return 0
        elif self.io.IO_readBit(Input.SENSOR_FLOOR1):
            return 1
        elif self.io.IO_readBit(Input.SENSOR_FLOOR1):
            return 2
        elif self.io.IO_readBit(Input.SENSOR_FLOOR1):
            return 3
        else:
            return -1

    def get_stop_signal(self):
        return self.io.IO_setBit(Input.STOP)


    def get_obstruction_signal(self):
        return self.io.IO_readBit(Input.OBSTRUCTION)