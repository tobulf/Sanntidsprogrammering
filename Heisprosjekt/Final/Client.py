from threading import Lock, Thread
from LightCtrl import *
from TypeClasses import *
from ButtonsPressed import *
from Order import Order
from ClientObject import Client
from Elevator import Elevator
from HTTPClient import HttpClient
from UDPServer import UdpServer
from Timer import Timer
import netifaces as FindIP
from time import sleep

# Finding IP
FindIP.ifaddresses('eth0')
Address = FindIP.ifaddresses('eth0')[2][0]['addr']
Port = 20011

# Declaring vital objects:
elevator = Elevator()
mutex = Lock()
Httpclient = HttpClient("", Port)
ClientObject = Client()
ClientUDP = UdpServer(Port)
RequestTimer = Timer()


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


def ButtonThread(RefreshRate = 0.1, PrintRate = 1):
    # Declare an orderobject to keep control of orders:
    OrderObject = Order()
    # Declaring Buttonobject, to poll buttons:
    Buttons = ButtonObject()
    printTimer = Timer()
    printTimer.StartTimer()
    while True:
        # Small print function to keep track of what state the elevator is in:
        if printTimer.GetCurrentTime() > PrintRate:
            printTimer.StartTimer()
            if ClientUDP.connected:
                print "___________________________________________"
                print "Currently being served by: ", ClientUDP.ServerAddress
            else:
                print "___________________________________________"
                print "Currently disconnected..."
        # Everything starts with polling on the Buttons:
        pressed = Buttons.ButtonPressed()
        # Basicaly a statemachine for the Client:
        # Need some sort of thing for the client to tell that an order has been served.
        if pressed and ClientUDP.connected:
            RequestTimer.StartTimer()
            floor, button, externalorder = pressed
            if externalorder:
                # Declare a ClientObject which contain all necessary information to the server:
                ClientObject = Client(Address=Address, Order=[floor, button], Direction=elevator.direction, Position=elevator.currentfloor, InternalOrders=elevator.InternalQueue, OrderCompleted=OrderObject.ExternalOrderServed(elevator.currentfloor, elevator.direction, elevator.currentstate), CurrentState=elevator.currentstate, OrderUp=OrderObject.orderUp, OrderDown=OrderObject.orderDown)
                # Using mutex before making a request, to prevent concurrency if the order never gets trough:
                ClientObject = Httpclient.PostRequest("GotOrder", ClientObject.toJson())
                if ClientObject:
                    # Add Potential order:
                    OrderObject.AppendOrder(ClientObject)
                    # Update external queues:
                    mutex.acquire()
                    elevator.ExternalQueueUp   = OrderObject.orderUp
                    elevator.ExternalQueueDown = OrderObject.orderDown
                    mutex.release()
                    # Set all the ligths:
                    for i in range(elevator.floors):
                        if ClientObject.lightsDown[i]:
                            SetLigth(i, LampType.CallDown)
                        if ClientObject.lightsUp[i]:
                            SetLigth(i, LampType.CallUp)
                        if not ClientObject.lightsDown[i]:
                            KillLight(i, LampType.CallDown)
                        if not ClientObject.lightsUp[i]:
                            KillLight(i, LampType.CallUp)
                elif not ClientObject:
                    # If the Client has issues submitting the order to the server it just takes the order itself:
                    if button == ButtonType.CallDown:
                        elevator.ExternalQueueDown[floor] = True
                        SetLigth(floor, ButtonType.CallDown)
                    if button == ButtonType.CallUp:
                        elevator.ExternalQueueUp[floor] = True
                        SetLigth(floor, ButtonType.CallUp)
            else:
                # if not an externalOrder, just add the order to internal queue:
                mutex.acquire()
                elevator.InternalQueue[floor] = True
                mutex.release()
                # Set the lights:
                SetLigth(floor, LampType.Command)
#
        elif not pressed and ClientUDP.connected and (RequestTimer.GetCurrentTime() > RefreshRate or not RequestTimer.started):
            # Reset the Request-timer:
            RequestTimer.StartTimer()
            # Check if any orders ar served
            OrderCompleted = OrderObject.ExternalOrderServed(elevator.currentfloor, elevator.direction, elevator.currentstate)
            # Declare a ClientObject which contain all necessary information to the server:
            ClientObject = Client(Address=Address, Direction = elevator.direction, Position=elevator.currentfloor, InternalOrders=elevator.InternalQueue, OrderCompleted=OrderCompleted, CurrentState=elevator.currentstate, OrderUp=OrderObject.orderUp, OrderDown=OrderObject.orderDown)
            ClientObject = Httpclient.PostRequest("GetUpdate", ClientObject.toJson())
            if ClientObject:
                # Add an potential order to the orderlist:
                OrderObject.AppendOrder(ClientObject)
                # Update external queues:
                mutex.acquire()
                elevator.ExternalQueueUp = OrderObject.orderUp
                elevator.ExternalQueueDown = OrderObject.orderDown
                mutex.release()
                # Reset the lights for the external orders:
                for i in range(elevator.floors):
                    if ClientObject.lightsDown[i]:
                        SetLigth(i, LampType.CallDown)
                    if ClientObject.lightsUp[i]:
                        SetLigth(i, LampType.CallUp)
                    if not ClientObject.lightsDown[i]:
                        KillLight(i, LampType.CallDown)
                    if not ClientObject.lightsUp[i]:
                        KillLight(i, LampType.CallUp)

        # If the Client is not connected to a server, it works as a ordinary elevator:
        elif pressed and not ClientUDP.connected:
            floor, button, externalorder = pressed
            # Mutex to prevent concurrency:
            mutex.acquire()
            if button == ButtonType.CallDown:
                elevator.ExternalQueueDown[floor] = True
                OrderObject.orderDown = elevator.ExternalQueueDown
                SetLigth(floor, ButtonType.CallDown)
            if button == ButtonType.CallUp:
                elevator.ExternalQueueUp[floor] = True
                OrderObject.orderUp = elevator.ExternalQueueUp
                SetLigth(floor, ButtonType.CallUp)
            if button == ButtonType.Command:
                elevator.InternalQueue[floor] = True
                SetLigth(floor, ButtonType.Command)
            mutex.release()
            
        elif not ClientUDP.connected:
            RequestTimer.StopTimer()
            # Turn of all lights that are not in the orderList:
            for i in range(elevator.floors):
                if not elevator.ExternalQueueUp[i]:
                    OrderObject.orderUp[i] = False
                    KillLight(i, ButtonType.CallUp)
                if not elevator.ExternalQueueDown[i]:
                    OrderObject.orderDown[i] = False
                    KillLight(i, ButtonType.CallDown)



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






