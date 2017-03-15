from ctypes import cdll





class Elev(object):
    def __init__(self):
        self.native = cdll.LoadLibrary("./elev.so")
        self.native.elev_init()

    def set_motordirection(self, dirn):
        self.native.elev_set_motor_direction(dirn)

    def set_button_lamp(self, button, floor, value):
        self.native.elev_set_button_lamp(button, floor, value)

    def set_floor_indicator(self, floor):
        self.native.elev_set_floor_indicator(floor)

    def set_door_open_lamp(self, value):
        self.native.elev_set_door_open_lamp(value)

    def set_stop_lamp(self, value):
        self.native.elev_set_stop_lamp(value)

    def get_buttonsignal(self, button, floor):
        return self.native.elev_get_button_signal(button, floor)

    def get_floor_sensor_signal(self):
        return self.native.elev_get_floor_sensor_signal()

    def get_stop_signal(self):
        return self.native.elev_get_stop_signal()

    def get_obstruction_signal(self):
        return self.native.elev_get_obstruction_signal()


elev = Elev()
