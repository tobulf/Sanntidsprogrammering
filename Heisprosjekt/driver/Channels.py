import comedi


#Basicly a blueprint of the channels.h that is given, divided into inputs and outputs
class Input:
    #in port 4
    PORT_4_SUBDEVICE        = 3
    PORT_4_CHANNEL_OFFSET   = 16
    PORT_4_DIRECTION        = comedi.INPUT
    OBSTRUCTION             = 0x300+23
    STOP                    = 0x300+22
    BUTTON_COMMAND1         = 0x300+21
    BUTTON_COMMAND2         = 0x300+20
    BUTTON_COMMAND3         = 0x300+19
    BUTTON_COMMAND4         = 0x300+18
    BUTTON_UP1              = 0x300+17
    BUTTON_UP2              = 0x300+16

    #in port 1
    PORT_1_SUBDEVICE        = 2
    PORT_1_CHANNEL_OFFSET   = 0
    PORT_1_DIRECTION        = comedi.INPUT
    BUTTON_DOWN2            = 0x200+0
    BUTTON_UP3              = 0x200+1
    BUTTON_DOWN3            = 0x200+2
    BUTTON_DOWN4            = 0x200+3
    SENSOR_FLOOR1           = 0x200+4
    SENSOR_FLOOR2           = 0x200+5
    SENSOR_FLOOR3           = 0x200+6
    SENSOR_FLOOR4           = 0x200+7
    #Lists of buttons and sensors:
    INTERNAL_BUTTONS        = [BUTTON_COMMAND1, BUTTON_COMMAND2, BUTTON_COMMAND3, BUTTON_COMMAND4]
    BUTTONS_UP              = [BUTTON_UP1, BUTTON_UP2, BUTTON_UP3]
    BUTTONS_DOWN            = [BUTTON_DOWN2, BUTTON_DOWN3, BUTTON_DOWN4]
    EXTERNAL_BUTTONS        = BUTTONS_UP + BUTTONS_DOWN
    SENSORS                 = [SENSOR_FLOOR1, SENSOR_FLOOR2, SENSOR_FLOOR3, SENSOR_FLOOR4]

class Output:
    #out port 3
    PORT_3_SUBDEVICE        = 3
    PORT_3_CHANNEL_OFFSET   = 8
    PORT_3_DIRECTION        = comedi.INPUT
    MOTORDIR                = 0x300+15
    LIGHT_STOP              = 0x300+14
    LIGHT_COMMAND1          = 0x300+13
    LIGHT_COMMAND2          = 0x300+12
    LIGHT_COMMAND3          = 0x300+11
    LIGHT_COMMAND4          = 0x300+10
    LIGHT_UP1               = 0x300+9
    LIGHT_UP2               = 0x300+8

    #out port 2
    PORT_2_SUBDEVICE        = 3
    PORT_2_CHANNEL_OFFSET   = 0
    PORT_2_DIRECTION        = comedi.INPUT
    LIGHT_DOWN2             = 0x300+7
    LIGHT_UP3               = 0x300+6
    LIGHT_DOWN3             = 0x300+5
    LIGHT_DOWN4             = 0x300+4
    LIGHT_DOOR_OPEN         = 0x300+3
    LIGHT_FLOOR_IND2        = 0x300+1
    LIGHT_FLOOR_IND1        = 0x300+0
    #Lists of lights:
    INTERNAL_LIGHTS         = [LIGHT_COMMAND1, LIGHT_COMMAND2, LIGHT_COMMAND3, LIGHT_COMMAND4]
    LIGHTS_UP               = [LIGHT_UP1, LIGHT_UP2, LIGHT_UP3]
    LIGHTS_DOWN             = [LIGHT_DOWN2, LIGHT_DOWN3, LIGHT_DOWN4]

    #out port 0
    MOTOR                   = 0x100+0
