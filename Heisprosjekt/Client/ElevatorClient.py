from threading import Lock,Thread
from time import sleep
from LightCtrl import *
from TypeClasses import *
from ButtonsPressed import ButtonsPressed
from Client import Client
from Elevator import Elevator
from HTTPClient import HttpClient
from UDPClient import UdpServer
from json import dumps


Address = "129.241.187.143"
Port = 20010
elevator = Elevator()
mutex = Lock()
Httpclient = HttpClient("", Port)
ClientObject = Client()
ClientUDP = UdpServer(Port)


def ElevatorThread():
    elevator.Serve()

def UDPThread():
    global Httpclient
    while True:
        ClientUDP.Listen()
        # If the Client is disconnected and has no HttpConnection:
        if ClientUDP.connected and not Httpclient.connected:
            # Connect the Httpclient
            mutex.acquire()
            Httpclient = HttpClient(ClientUDP.ServerAddress, Port)
            Httpclient.connected = True
            mutex.release()
        # To reset the Client if it gets disconnected:
        elif not ClientUDP.connected and Httpclient.connected:
            mutex.acquire()
            Httpclient.connected = False
            mutex.release()


def ButtonThread():
    while True:
        pressed = ButtonsPressed()
        # Basicaly a statemachine for the Client:
        # Need some sort of thing for the client to tell that an order has been served.
        if pressed and ClientUDP.connected:
            floor, button, externalorder = pressed
            if externalorder:
                mutex.acquire()
                ClientObject = Client(Address=Address, Order=[floor, elevator.direction], Direction=elevator.direction, Position = elevator.currentfloor, InternalOrders = elevator.InternalQueue)
                mutex.release()
                # Using mutex before making a request, to prevent concurrency if the order never gets trough:
                ClientObject = Httpclient.PostRequest("GotOrder", ClientObject.toJson())
                mutex.acquire()
                if ClientObject:
                    # Updating the orders with latest version:
                    elevator.ExternalQueueUp   = ClientObject.orderUp
                    elevator.ExternalQueueDown = ClientObject.orderDown
                mutex.release()
                # Need to add lights here:
            else:
                # if not an externalOrder, just add the order to internal queue:
                mutex.acquire()
                elevator.InternalQueue[floor] = True
                mutex.release()
                # Set the lights:
                SetLigth(floor, LampType.ButtonCommand)

        elif not pressed and ClientUDP.connected:
            mutex.acquire()
            ClientObject = Client(Address=Address, Direction = elevator.direction, Position = elevator.currentfloor, InternalOrders = elevator.InternalQueue)
            mutex.release()
            ClientObject = Httpclient.PostRequest("GetUpdate", ClientObject.toJson())

            if ClientObject:
                #print dumps(ClientObject.lightsDown), dumps(ClientObject.lightsUp)
                mutex.acquire()
                elevator.ExternalQueueUp = ClientObject.orderUp
                elevator.ExternalQueueDown = ClientObject.orderDown
                mutex.release()
                #print dumps(elevator.ExternalQueueDown), dumps(elevator.ExternalQueueUp)
                # Reset the lights for the external orders:
                for i in range(elevator.floors):
                    if ClientObject.lightsDown[i]:
                        SetLigth(i, LampType.ButtonCallDown)
                    elif ClientObject.lightsUp[i]:
                        SetLigth(i, LampType.ButtonCallUp)
                    elif not ClientObject.lightsDown[i]:
                        KillLight(i, LampType.ButtonCallDown)
                    elif not ClientObject.lightsDown[i]:
                        KillLight(i, LampType.ButtonCallUp)


        # If the Client is not connected to a server, it works as a ordinary elevator:
        elif pressed and not ClientUDP.connected:
            floor, button, externalorder = pressed
            mutex.acquire()
            if button == Button_type.BUTTON_CALL_DOWN:
                elevator.ExternalQueueDown[floor] = True
                SetLigth(floor, Button_type.BUTTON_CALL_DOWN)
            if button == Button_type.BUTTON_CALL_UP:
                elevator.ExternalQueueUp[floor] = True
                SetLigth(floor, Button_type.BUTTON_CALL_UP)
            if button == Button_type.BUTTON_COMMAND:
                elevator.InternalQueue[floor] = True
                SetLigth(floor, Button_type.BUTTON_COMMAND)
            mutex.release()
            
        elif not ClientUDP.connected:
            # Turn of all lights that are not in the orderList:
            for i in range(elevator.floors):
                if not elevator.ExternalQueueUp[i]:
                    KillLight(i, Button_type.BUTTON_CALL_UP)
                if not elevator.ExternalQueueDown[i]:
                    KillLight(i, Button_type.BUTTON_CALL_DOWN)







def main():
    # Declaring all threads;
    Thread1 = Thread(target = ButtonThread, args = (),)
    Thread2 = Thread(target = ElevatorThread, args = (),)
    Thread3 = Thread(target = UDPThread, args = (),)
    # Starting threads
    Thread1.start()
    Thread2.start()
    Thread3.start()
    # wait for Threads to finish, if so its something wrong.
    Thread1.join()
    Thread2.join()
    Thread3.join()


main()






