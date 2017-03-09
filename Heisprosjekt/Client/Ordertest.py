from Order import Order
from TypeClasses import*

x = [0, LampType.ButtonCallDown]

order = Order()

order.AppendOrder(x)

print order.ExternalOrderServed(0, Motor_direction.DIRN_DOWN)
print order.orderDown