from Elev import elev
from Client import Client



# Kills all the lights when the elevator arrives at a floor
def KillLights(Floor):
    for i in range(3):
        elev.set_button_lamp(i, Floor, 0)

def SetLigth(Floor, LampType):
    elev.set_button_lamp(LampType, Floor, 1)
