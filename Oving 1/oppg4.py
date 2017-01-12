# Python 3.3.3 and 2.7.6
# python helloworld_python.py

from threading import Thread

i = 0

def ThreadFunction_1():
    for n in range (0,1000000):
        global i 
        i -= 1


def ThreadFunction_2():
    for n in range (0,1000000):
        global i 
        i += 1

# Potentially useful thing:
#   In Python you "import" a global variable, instead of "export"ing it when you declare it
#   (This is probably an effort to make you feel bad about typing the word "global")

def main():
    Thread_1 = Thread(target = ThreadFunction_1, args = (),)
    Thread_2 = Thread(target = ThreadFunction_2, args = (),)
    Thread_1.start()
    Thread_2.start()
    
    Thread_1.join()
    Thread_2.join()
    print(i)

main()