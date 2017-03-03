from Elevator import elev

def ButtonsPressed():
    for i in range(4):
        for n in range(3):
            if elev.get_buttonsignal(n,i):
                if n == 0 or n == 1:
                    return (i, n, True)
                else:
                    return (i, n, False)
    return False








