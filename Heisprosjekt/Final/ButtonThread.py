from threading import Lock, Thread
from LightCtrl import *
from TypeClasses import *
from ButtonsPressed import *
import subprocess as Respawn
from Order import Order
from ClientObject import Client
from Elevator import Elevator
from HTTPClient import HttpClient
from UDPServer import UdpServer
from Timer import Timer
import netifaces as FindIP


class HttpThread(object):
    def __init__(self):
        self.OrderObject = Order()
        self.Buttons = ButtonObject()
        self.printTimer = Timer()
        self.printTimer.StartTimer()
        self.FindIP.ifaddresses('eth0')
        self.Address = FindIP.ifaddresses('eth0')[2][0]['addr']
        self.Port = 20011
        
    def Run(self, elevator, ClientUDP, PrintRate = 1):
        while True:
        # Everything starts with polling on the Buttons:
        pressed = self.Buttons.ButtonPressed()
        # Basicaly a statemachine for the Client:
        if pressed and ClientUDP.connected:
            RequestTimer.StartTimer()
            floor, button, externalorder = pressed
            if externalorder:
                # Declare a ClientObject which contain all necessary information to the server:
                ClientObject = Client(Address=Address, Order=[floor, button], Direction=elevator.direction,
                                      Position=elevator.currentfloor, InternalOrders=elevator.InternalQueue,
                                      OrderCompleted=self.OrderObject.ExternalOrderServed(elevator.currentfloor, elevator.direction, elevator.currentstate),
                                      CurrentState=elevator.currentstate, OrderUp=self.OrderObject.orderUp, OrderDown=self.OrderObject.orderDown)
                # Using mutex before making a request, to prevent concurrency if the order never gets trough:
                self.ClientObject = Httpclient.PostRequest("GotOrder", ClientObject.toJson())
                if ClientObject:
                    # Add Potential order:
                    self.OrderObject.AppendOrder(ClientObject)
                    # Update external queues:
                    mutex.acquire()
                    elevator.ExternalQueueUp   = self.OrderObject.orderUp
                    elevator.ExternalQueueDown = self.OrderObject.orderDown
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

        elif not pressed and ClientUDP.connected and (RequestTimer.GetCurrentTime() > RefreshRate or not RequestTimer.started):
            # Reset the Request-timer:
            RequestTimer.StartTimer()
            # Check if any orders ar served
            OrderCompleted = self.OrderObject.ExternalOrderServed(elevator.currentfloor, elevator.direction, elevator.currentstate)
            # Declare a ClientObject which contain all necessary information to the server:
            ClientObject = Client(Address=Address, Direction = elevator.direction, Position=elevator.currentfloor,
                                  InternalOrders=elevator.InternalQueue, OrderCompleted=OrderCompleted,
                                  CurrentState=elevator.currentstate, OrderUp=self.OrderObject.orderUp,
                                  OrderDown=self.OrderObject.orderDown)
            ClientObject = Httpclient.PostRequest("GetUpdate", ClientObject.toJson())
            # Check if there are a Clientobject:
            if ClientObject:
                # Add an potential order to the orderlist:
                self.OrderObject.AppendOrder(ClientObject)
                # Update external queues:
                mutex.acquire()
                elevator.ExternalQueueUp = self.OrderObject.orderUp
                elevator.ExternalQueueDown = self.OrderObject.orderDown
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
                self.OrderObject.orderDown = elevator.ExternalQueueDown
                SetLigth(floor, ButtonType.CallDown)
            if button == ButtonType.CallUp:
                elevator.ExternalQueueUp[floor] = True
                self.OrderObject.orderUp = elevator.ExternalQueueUp
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
                    self.OrderObject.orderUp[i] = False
                    KillLight(i, ButtonType.CallUp)
                if not elevator.ExternalQueueDown[i]:
                    self.OrderObject.orderDown[i] = False
                    KillLight(i, ButtonType.CallDown)
        # Kills the Network if the elevator has gone into errormode:
        if elevator.currentstate == ElevatorState.Error:
            # Send the latest state:
            ClientObject = Client(Address=Address, Direction=elevator.direction, Position=elevator.currentfloor,
                                  InternalOrders=elevator.InternalQueue, OrderCompleted=OrderCompleted,
                                  CurrentState=elevator.currentstate, OrderUp=self.OrderObject.orderUp,
                                  OrderDown=self.OrderObject.orderDown)
            Httpclient.PostRequest("GetUpdate", ClientObject.toJson())
            Respawn.Popen(["gnome-terminal", "-x", "sh", "-c", "python RunClient.py"])
            break

        # Small print function to keep track of what state the elevator is in:
        if self.printTimer.GetCurrentTime() > PrintRate:
            self.printTimer.StartTimer()
            if ClientUDP.connected:
                print "___________________________________________"
                print "Currently being served by: ", ClientUDP.ServerAddress
            else:
                print "___________________________________________"
                print "Currently disconnected..."
    


