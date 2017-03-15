from Elevator import elev


class ButtonObject(object):
    def __init__(self):
        self.pressed     = False


    def ButtonPressed(self):
        value = self.ButtonsPressed()
        if self.pressed and value:
            return False
        elif not self.pressed and value:
            self.pressed = True
            return value
        elif not value:
            self.pressed = False



    def ButtonsPressed(self):
        for i in range(4):
            for n in range(3):
                if elev.get_buttonsignal(n,i):
                    if n == 0 or n == 1:
                        return (i, n, True)
                    else:
                        return (i, n, False)
        return False



def ButtonsPressedd():
    for i in range(4):
        for n in range(3):
            if elev.get_buttonsignal(n,i):
                if n == 0 or n == 1:
                    return (i, n, True)
                else:
                    return (i, n, False)
    return False





