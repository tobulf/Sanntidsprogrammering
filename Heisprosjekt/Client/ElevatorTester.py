from Elevator import Elevator
from threading import Lock,Thread
from ButtonsPressed import ButtonsPressed


elevator = Elevator()
mutex = Lock()


def ElevatorThread():
    elevator.Serve()

def ButtonThread():
    while True:
        pressed = ButtonsPressed()
        #print dumps(elevator.Queue)
        if pressed:
            floor, button, externalorder = pressed
            if externalorder:


            else:
                mutex.aquire()
                elevator.InternalQueue[floor] = True



def main():
    Thread_1 = Thread(target = ButtonThread, args = (),)
    Thread_2 = Thread(target = ElevatorThread, args = (),)
    Thread_1.start()
    Thread_2.start()

    Thread_1.join()
    Thread_2.join()

main()






