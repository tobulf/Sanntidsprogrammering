from Elev import elev




# Kills light at specific type at specific floor
def KillLight(Floor, ButtonType):
    elev.set_button_lamp(ButtonType, Floor, 0)

# Lights specific light at specific floor.
def SetLigth(Floor, LampType):
    elev.set_button_lamp(LampType, Floor, 1)
