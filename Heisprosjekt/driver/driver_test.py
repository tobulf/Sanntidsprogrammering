from driver import Driver
from time import sleep

elevator = Driver()


elevator.set_floor_indicator(0)
while True:
    print "k"
    if elevator.get_buttonsignal(0,0):
        sleep(0.5)
        print


