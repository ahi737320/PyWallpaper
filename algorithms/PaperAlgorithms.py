import cairo
from time import sleep
import math
from algorithms.Helpers import hex_to_RGB
import random

hex_colours=[0x50514f, 0xf25f5c, 0xffe066, 0x247ba0, 0x70c1b3]
colours_large=[hex_to_RGB(i) for i in hex_colours]
colours=[]
for i in range(len(colours_large)):
    colours.append((colours_large[i][0]/255., colours_large[i][1]/255., colours_large[i][2]/255.))

def Circles(size, progress_queue):
    print(colours)
    surface=cairo.ImageSurface(cairo.FORMAT_RGB24, size[0], size[1])
    cc=cairo.Context(surface)
    max_radius = min(size)//2
    cc.set_source_rgb(*colours[0])
    cc.rectangle(0, 0, size[0], size[1])
    cc.fill()
    circles=[]
    while True:
        (x, y, radius) = create_non_intersecting_circle(0, size[0], 0, size[1], 8, max_radius, circles)
        if radius <= 0: break
        circles.append((x, y, radius))
        for colour in colours[1:]:
            cc.set_source_rgb(*colour)
            cc.arc(x, y, radius, 0, 2*math.pi)
            cc.fill()
            if radius <= 16:
                break
            radius = random.randint(8, radius-4)
    progress_queue.put((1, surface))


def create_non_intersecting_circle(minx, maxx, miny, maxy, minr, maxr, circles):
    import random

    for try_index in range(0, 20):
        x = random.randint(minx, maxx)
        y = random.randint(miny, maxy)
        r = random.randint(minr, maxr)
        if not check_if_circle_intersects(x, y, r, circles):
            return x, y, r
    return 0, 0, 0


def check_if_circle_intersects(x, y, r, circles):
    for (x2, y2, r2) in circles:
        if math.sqrt((x-x2)**2+(y-y2)**2) < (r + r2):
            return True
    return False
