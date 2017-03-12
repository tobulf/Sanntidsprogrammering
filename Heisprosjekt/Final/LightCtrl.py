from Elev import elev
from ClientObject import Client



# Kills all the lights when the elevator arrives at a floor
def KillLight(Floor, ButtonType):
    elev.set_button_lamp(ButtonType, Floor, 0)

def SetLigth(Floor, LampType):
    elev.set_button_lamp(LampType, Floor, 1)
