import comedi
from Channels import Input, Output
#Basicly a blueprint of the IO.c Written in python

class IO:
    comedi = None
    status = 0
    def __init__(self):
        self.comedi=comedi.open('/dev/comedi0')
        for i in range(8):
            self.status |= comedi.dio_config(self.comedi, Input.PORT_1_SUBDEVICE, i + Input.PORT_1_CHANNEL_OFFSET, Input.PORT_1_DIRECTION)
            self.status |= comedi.dio_config(self.comedi, Input.PORT_2_SUBDEVICE, i + Input.PORT_2_CHANNEL_OFFSET, Input.PORT_2_DIRECTION)
            self.status |= comedi.dio_config(self.comedi, Input.PORT_3_SUBDEVICE, i + Input.PORT_3_CHANNEL_OFFSET, Input.PORT_3_DIRECTION)
            self.status |= comedi.dio_config(self.comedi, Input.PORT_4_SUBDEVICE, i + Input.PORT_4_CHANNEL_OFFSET, Input.PORT_4_DIRECTION)

    def IO_setBit(self, channel, value):
        comedi.dio_write(self.comedim, channel >> 8, channel & 0xff, 0)

    def IO_clearBit(self, channel):
        comedi.dio_write(self.comedi, channel >> 8, channel & 0xff, 0)

    def IO_readBit(self, channel):
        return comedi.dio_read(self.comedi, channel >> 8, channel & 0xff)

