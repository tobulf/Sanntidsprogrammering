from ctypes import cdll





class Elev(object):
    def __init__(self):
        self.native = cdll.LoadLibrary("./elev.so")
        self.native.elev_init()

    def SetMotordirection(self, dirn):
        self.native.elev_set_motor_direction(dirn)

    def SetButtonLamp(self, button, floor, value):
        self.native.elev_set_button_lamp(button, floor, value)

    def SetFloorIndicator(self, floor):
        self.native.elev_set_floor_indicator(floor)

    def SetDoorOpenLamp(self, value):
        self.native.elev_set_door_open_lamp(value)

    def SetStopLamp(self, value):
        self.native.elev_set_stop_lamp(value)

    def GetButtonsignal(self, button, floor):
        return self.native.elev_get_button_signal(button, floor)

    def GetFloorSensorSignal(self):
        return self.native.elev_get_floor_sensor_signal()

    def GetStopSignal(self):
        return self.native.elev_get_stop_signal()

    def GetObstructionSignal(self):
        return self.native.elev_get_obstruction_signal()


elev = Elev()
