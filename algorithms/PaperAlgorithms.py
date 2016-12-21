import cairo
from time import sleep
import math
from algorithms.Helpers import *
import random

hex_colours=[0x50514f, 0xf25f5c, 0xffe066, 0x247ba0, 0x70c1b3]
colours_large=[hex_to_RGB(i) for i in hex_colours]
colours=[]
for i in range(len(colours_large)):
    colours.append((colours_large[i][0]/255., colours_large[i][1]/255., colours_large[i][2]/255.))

def Circles(size, palette, progress_queue):
    surface=cairo.ImageSurface(cairo.FORMAT_RGB24, size[0], size[1])
    cc=cairo.Context(surface)
    max_radius = min(size)//2
    cc.set_source_rgb(*colours[0])
    cc.rectangle(0, 0, size[0], size[1])
    cc.fill()
    circles=[]
    progress_queue.put((1, surface))

def Squares(size, progress_queue):
    l_x=size[0]/10
    l_y=size[1]/10
    surface=cairo.ImageSurface(cairo.FORMAT_RGB24, size[0], size[1])
    cc=cairo.Context(surface)
    points=[]
    for i in range(12):
        points.append([])
        for j in range(12):
            points[i].append(Point(l_x*(i-1), l_y*(j-1)))
            points[i][j].randomise(l_x/3, l_y/3)

    for i in range(11):
        for j in range(11):
            cc.set_source_rgb(*choice(colours))
            p1 = (points[i][j].x, points[i][j].y)
            p2 = (points[i+1][j].x, points[i+1][j].y)
            p3 = (points[i+1][j+1].x, points[i+1][j+1].y)
            p4 = (points[i][j+1].x, points[i][j+1].y)

            cc.new_path()
            cc.move_to(*p1)
            cc.line_to(*p2)
            cc.line_to(*p3)
            cc.line_to(*p4)
            cc.close_path()
            cc.fill()

            lines=[(p1, p2), (p2, p3), (p3, p4), (p4, p1)]
            for line in lines:
                cc.new_path()
                cc.move_to(*line[0])
                cc.line_to(*line[1])
                cc.stroke()

    progress_queue.put((1, surface))
