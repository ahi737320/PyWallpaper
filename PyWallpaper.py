#!/usr/bin/env python3
#Python script that generates wallpapers

import tkinter as tk
import tkinter.ttk as ttk
import importlib
import algorithms.PaperAlgorithms as pa
from algorithms.Helpers import *
from algorithms.Colours import *
from threading import Thread
from queue import Queue
from PIL import ImageTk, Image

TMP_IMAGE_LOCATION='/tmp/pywallpaper-image.png'
generators={'Circles':pa.Circles}
generator_running=False

def run_generator(gen_type, queue, arguments):
    gen_thread=Thread(target=generators[gen_type], args=arguments+[queue])
    gen_thread.start()
    generator_running=True

class Squares(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

class Circles(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

class Palette(tk.Frame):
    def __init__(self, parent, palette, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.palette_name = tk.Label(self, text=palette[0])
        self.palette_name.grid(row=0, column=0, sticky='news')
        self.colours=[]
        for i in range(len(palette[1])):
            self.colours.append(tk.Label(self, text=palette[1][i], bg=palette[1][i]))
            self.colours[i].grid(row=0, column=(i+1))
        self.separator=ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(row=1, column=0, columnspan=len(self.colours)+1, sticky='ew')

class CustomPalette(tk.Frame):
    def __init__(self, parent, initial_palette, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initial_palette=initial_palette
        self.colours=Palette(self, ["Custom", self.initial_palette])
        self.colours.grid(row=0, column=0)

class Colours(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.downloaded_palettes=tk.Frame(self)
        self.downloaded_palettes.grid(row=0, column=0)
        self.raw_palettes = get_palettes(20)
        self.palettes=[]
        for i in range(len(self.raw_palettes)):
            self.palettes.append(Palette(self.downloaded_palettes, self.raw_palettes[i]))
            self.palettes[i].grid(row=i, column=0)
        self.custom_palette = CustomPalette(self, [('#ffffff')]*6)
        self.custom_palette.grid(row=1, column=0)

class Generator(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.selector=ttk.Combobox(self, state="readonly", values=list(generators.keys()))
        self.selector.set(list(generators.keys())[0])
        self.selector.grid(row=0, column=0, columnspan=4)
        self.x_label=tk.Label(self, text="x resolution:")
        self.x_label.grid(row=1, column=0)
        self.x=tk.StringVar(self, "1920")
        self.x_res=tk.Entry(self, textvariable=self.x)
        self.x_res.grid(row=1, column=1)
        self.y_label=tk.Label(self, text="y resolution:")
        self.y_label.grid(row=1, column=2)
        self.y=tk.StringVar(self, "1080")
        self.y_res=tk.Entry(self, textvariable=self.y)
        self.y_res.grid(row=1, column=3)

class Viewer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image_label=tk.Label(self, text="No image")
        self.image_label.pack(expand=True, fill="both")

class PyWallpaper(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.queue=Queue()
        self.parent=parent
        self.notebook=ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, columnspan=2)
        self.generate_button=tk.Button(self, text="Generate Pattern", command=self.generate_image)
        self.generate_button.grid(row=1, column=0)
        self.generate_button.configure(state=tk.NORMAL)
        self.percentage=tk.DoubleVar(0)
        self.percentage_indicator=ttk.Progressbar(self, orient="horizontal", mode="determinate", variable=self.percentage)
        self.percentage_indicator.grid(row=1, column=1)
        self.generator=Generator(self.notebook)
        self.generator.grid(row=0, column=0)
        self.surface=None
        self.viewer=Viewer(self.notebook)
        self.viewer.grid(row=0, column=0)
        self.colours=Colours(self.notebook)
        self.colours.grid(row=0, column=0)
        self.notebook.add(self.generator, text='Generator')
        self.notebook.add(self.viewer, text='Viewer')
        self.notebook.add(self.colours, text='Colours')

    def generate_image(self):
        try:
            x=int(self.generator.x.get())
            y=int(self.generator.y.get())
            if not generator_running:
                self.surface=None
                self.generate_button.configure(state=tk.DISABLED)
                self.percentage.set(0)
                run_generator(self.generator.selector.get(), self.queue, [(x, y)])
                self.check_generation()
        except:
            pass

    def check_generation(self):
        got_surface=False
        while not self.queue.empty():
            new_item=self.queue.get()
            self.queue.task_done()
            if new_item[0]==0:
                self.percentage.set(new_item[1])
            elif new_item[0]==1:
                self.surface=new_item[1]
                self.viewer.surface=self.surface
                got_surface=True
        if not got_surface: self.after(1000, self.check_generation)
        else: self.post_generation()

    def post_generation(self):
        self.surface.write_to_png(TMP_IMAGE_LOCATION)
        self.img=ImageTk.PhotoImage(Image.open(TMP_IMAGE_LOCATION).resize((300, 300), Image.ANTIALIAS))
        self.generate_button.configure(state=tk.NORMAL)
        self.viewer.image_label.configure(text=None, image=self.img)
        generator_running=False

def main():
    root=tk.Tk()
    app=PyWallpaper(root)
    app.grid()
    root.mainloop()

if __name__=='__main__':
    main()
