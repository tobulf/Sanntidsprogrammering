from threading import Lock,Thread
from LightCtrl import *
from TypeClasses import *
from ButtonsPressed import ButtonsPressed
from Order import Order
from Client import Client
from Elevator import Elevator
from HTTPClient import HttpClient
from UDPClient import UdpServer
from time import sleep



Address = "129.241.187.151"
Port = 20011
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
    # Declare an orderobject to keep control of orders:

    OrderObject = Order()
    while True:
        pressed = ButtonsPressed()
        # Basicaly a statemachine for the Client:
        # Need some sort of thing for the client to tell that an order has been served.
        if pressed and ClientUDP.connected:
            floor, button, externalorder = pressed
            if externalorder:
                ClientObject = Client(Address=Address, Order=[floor, elevator.direction], Direction=elevator.direction, Position = elevator.currentfloor, InternalOrders = elevator.InternalQueue, OrderCompleted = OrderObject.ExternalOrderServed(elevator.currentfloor, elevator.direction, elevator.currentstate))
                # Using mutex before making a request, to prevent concurrency if the order never gets trough:
                ClientObject = Httpclient.PostRequest("GotOrder", ClientObject.toJson())
                mutex.acquire()
                if ClientObject:
                    # Add Potential order:
                    OrderObject.AppendOrder(ClientObject.order)
                    # Update external queues
                    elevator.ExternalQueueUp   = OrderObject.orderUp
                    elevator.ExternalQueueDown = OrderObject.orderDown
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
            orderc = OrderObject.ExternalOrderServed(elevator.currentfloor, elevator.direction, elevator.currentstate)
            print orderc
            print OrderObject.orderUp, OrderObject.orderDown, elevator.currentfloor, elevator.direction, elevator.currentstate
            ClientObject = Client(Address=Address, Direction = elevator.direction, Position = elevator.currentfloor, InternalOrders = elevator.InternalQueue, OrderCompleted = orderc)
            ClientObject = Httpclient.PostRequest("GetUpdate", ClientObject.toJson())
            if ClientObject:
                print ClientObject.order
                OrderObject.AppendOrder(ClientObject.order)
                mutex.acquire()
                elevator.ExternalQueueUp = OrderObject.orderUp
                elevator.ExternalQueueDown = OrderObject.orderDown
                mutex.release()
                # Reset the lights for the external orders:
                #print ClientObject.lightsDown, ClientObject.lightsUp
                for i in range(elevator.floors):
                    if ClientObject.lightsDown[i]:
                        SetLigth(i, LampType.ButtonCallDown)
                    if ClientObject.lightsUp[i]:
                        SetLigth(i, LampType.ButtonCallUp)
                    if not ClientObject.lightsDown[i]:
                        KillLight(i, LampType.ButtonCallDown)
                    if not ClientObject.lightsUp[i]:
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







def MainThread():
    # Declaring all threads;
    Thread1 = Thread(target = ButtonThread, args = (),)
    Thread2 = Thread(target = ElevatorThread, args = (),)
    Thread3 = Thread(target = UDPThread, args = (),)
    # Making all threads Sub-Threads
    Thread1.daemon = True
    Thread2.daemon = True
    Thread3.daemon = True
    # Starting threads
    Thread1.start()
    Thread2.start()
    Thread3.start()
    # Keep the main Thread Alive:
    while True:
        pass


MainThread()






