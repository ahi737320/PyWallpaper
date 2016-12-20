from random import *

def hex_to_RGB(hex_value):
    return ((hex_value>>8>>8)%256, (hex_value>>8)%256, hex_value%256)

class Point:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def randomise(self, range_x, range_y):
        self.x+=range_x*2*random()-1
        self.y+=range_y*2*random()-1
