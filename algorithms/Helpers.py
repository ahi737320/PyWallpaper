from random import *

def hex_to_RGB(hex_value):
    return ((hex_value>>8>>8)%256, (hex_value>>8)%256, hex_value%256)

def text_hex_to_RGB(text_hex):
    int_value=int(text_hex[1:], 16)
    return hex_to_RGB(int_value)

def RGB_to_hex(rgb):
    return hex((rgb[0]<<16)+(rgb[1]<<8)+rgb[2])

def RGB_to_text_hex(rgb):
    return ('#'+RGB_to_hex(rgb)[2:])

def push_hex_values(text_hex, shift):
    rgb=text_hex_to_RGB(text_hex)
    new_rgb=[(i+shift)%256 for i in rgb]
    return RGB_to_text_hex(new_rgb)

class Point:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def randomise(self, range_x, range_y):
        self.x+=range_x*2*random()-1
        self.y+=range_y*2*random()-1
