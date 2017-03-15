from Elevator import Elevator

from threading import Lock,Thread
from ButtonsPressed import ButtonsPressed
from LightCtrl import *


from Queue import Queue
from threading import Lock,Thread
from TypeClasses import *
from ButtonsPressed import ButtonsPressed
from LightCtrl import *
from time import sleep
from json import dumps
from Elev import elev

elevator = Elevator()
mutex = Lock()


def ElevatorThread():
    elevator.Serve()

def ButtonThread():
    while True:
        pressed = ButtonsPressed()
        #print dumps(elevator.Queue)
        if pressed:
            floor, button = pressed
            mutex.acquire()
            elevator.Queue[button][floor] = True
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






