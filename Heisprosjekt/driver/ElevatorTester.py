from Elevator import Elevator
from Queue import Queue
from threading import Lock,Thread
from TypeClasses import *
from ButtonsPressed import ButtonsPressed
from LightCtrl import *
from time import sleep
from Elev import elev
elevator = Elevator()
mutex = Lock()


def ElevatorThread():
    elevator.Serve()

def ButtonThread():
    while True:
        pressed = ButtonsPressed()
        if pressed:
            floor, button = pressed
            mutex.acquire()
            elevator.Queue[floor] = True
            mutex.release()
            SetLigth(floor, button)
        else:
            pass




def main():
    Thread_1 = Thread(target = ButtonThread, args = (),)
    Thread_2 = Thread(target = ElevatorThread, args = (),)
    Thread_1.start()
    Thread_2.start()

    Thread_1.join()
    Thread_2.join()

main()






