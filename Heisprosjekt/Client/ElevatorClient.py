from threading import Lock,Thread
from LightCtrl import *
from TypeClasses import *
from ButtonsPressed import ButtonsPressed
from Client import Client
from Elevator import Elevator
from Sanntidsprogrammering.Heisprosjekt.Client.HTTPClient import HttpClient

Address = "129.241.187.146"
Port = 20010
elevator = Elevator()
mutex = Lock()
Httpclient = HttpClient()
ClientObject = Client()



def ElevatorThread():
    elevator.Serve()

def UDPThread():



def ButtonThread():
    while True:
        pressed = ButtonsPressed()
        #print dumps(elevator.Queue)
        if pressed:
            floor, button, externalorder = pressed
            if externalorder:
                mutex.aquire()
                ClientObject = Client(Order=[floor, elevator.direction], Direction=elevator.direction, Position = elevator.currentfloor, InternalOrders = elevator.InternalQueue, Address=Address)
                mutex.release()
                # Using mutex before making a request, to prevent concurrency if the order never gets trough:
                ClientObject = Httpclient.PostRequest("Got Order", ClientObject.toJson())
                mutex.aquire()
                # Updating the orders with latest version:
                elevator.ExternalQueueUp   = ClientObject.orderUp
                elevator.ExternalQueueDown = ClientObject.orderDown
                mutex.release()
                # Need to add lights here:
            else:
                mutex.aquire()
                elevator.InternalQueue[floor] = True
                mutex.release()
        else:
            mutex.aquire()
            ClientObject = Client(Direction = elevator.direction, Position = elevator.currentfloor, InternalOrders = elevator.InternalQueue)
            mutex.release()
            ClientObject = Httpclient.PostRequest("Get Update", ClientObject.toJson())
            mutex.aquire()
            elevator.ExternalQueueUp = ClientObject.orderUp
            elevator.ExternalQueueDown = ClientObject.orderDown
            mutex.release()
            # Set the lights for the external orders:
            for i in range(elevator.floors):
                if ClientObject.lightsDown[i]:
                    SetLigth(i, Lamp_type.BUTTON_CALL_DOWN)
                elif ClientObject.lightsUp[i]:
                    SetLigth(i, Lamp_type.BUTTON_CALL_UP)






def main():
    Thread_1 = Thread(target = ButtonThread, args = (),)
    Thread_2 = Thread(target = ElevatorThread, args = (),)
    Thread_1.start()
    Thread_2.start()

    Thread_1.join()
    Thread_2.join()

main()






