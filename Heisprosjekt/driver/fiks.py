from elev import Elev
from ctypes import cdll


native = cdll.LoadLibrary("./elev.so")

elev = Elev(native)
