from Elevator import elev

def ButtonsPressed():
    for i in range(4):
        for n in range(3):
            if elev.get_buttonsignal(n,i):
                return (i, n)
    return False








