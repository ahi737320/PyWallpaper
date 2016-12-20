import cairo

colours=[0x50514f, 0xf25f5c, 0xffe066, 0x247ba0, 0x70c1b3]
def Circles(size, progress_queue):
    surface=cairo.ImageSurface(cairo.FORMAT_RGB24, size[0], size[1])
    cc=cairo.Context(surface)
    cc.set_source_rgb(0, 0, 0)
    cc.rectangle(0, 0, size[0], size[1])
    cc.fill()
    cc.set_source_rgb(20, 245, 200)
    cc.rectangle(300, 300, 900, 900)
    cc.fill()
    surface.write_to_png("tester")
