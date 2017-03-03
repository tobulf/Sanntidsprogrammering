from time import time



class Timer(object): #Timer object
    def __init__(self):
        self.start = 0
        self.started = False

    def StartTimer(self):
        self.start = time()
        self.started = True
    def GetCurrentTime(self):
        if self.started:
            return time() - self.start
        else:
            return 0

    def StopTimer(self):
        self.started = False

    def WaitNSeconds(self, N):
        self.start = time()
        while time() - self.start < N:
            pass



