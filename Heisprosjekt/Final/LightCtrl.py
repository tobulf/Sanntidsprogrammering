from Elev import elev




# Kills light at specific type at specific floor
def KillLight(Floor, ButtonType):
    elev.SetButtonLamp(ButtonType, Floor, 0)

# Lights specific light at specific floor.
def SetLigth(Floor, LampType):
    elev.SetButtonLamp(LampType, Floor, 1)
