#!/usr/bin/env python3
#Python script that generates wallpapers

import tkinter as tk
import tkinter.ttk as ttk
import importlib
from algorithms.PaperAlgorithms import Circles
from algorithms.Helpers import *
from threading import Thread
from queue import Queue
from PIL import ImageTk, Image

TMP_IMAGE_LOCATION='/tmp/pywallpaper-image.png'
generators={'Circles':0, 'Triangles':1}
generator_running=False

def run_generator(gen_type, queue, arguments):
    gen_thread=Thread(target=Circles, args=arguments+[queue])
    gen_thread.start()
    generator_running=True

class Circle(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

class Generator(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.selector=ttk.Combobox(self, state="readonly", values=list(generators.keys()))
        self.selector.set(list(generators.keys())[0])
        self.selector.grid(row=0, column=0, columnspan=4)
        self.x_label=tk.Label(self, text="x resolution:")
        self.x_label.grid(row=1, column=0)
        self.x_res=tk.Entry(self)
        self.x_res.grid(row=1, column=1)
        self.y_label=tk.Label(self, text="y resolution:")
        self.y_label.grid(row=1, column=2)
        self.y_res=tk.Entry(self)
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
        self.notebook.add(self.generator, text='Generator')
        self.notebook.add(self.viewer, text='Viewer')

    def generate_image(self):
        if not generator_running:
            self.surface=None
            self.generate_button.configure(state=tk.DISABLED)
            self.percentage.set(0)
            run_generator("Circles", self.queue, [(1920, 1080)])
            self.check_generation()

    def check_generation(self):
        got_surface=False
        while not self.queue.empty():
            new_item=self.queue.get()
            self.queue.task_done()
            if new_item[0]==0: self.percentage.set(new_item[1])
            elif new_item[0]==1:
                self.surface=new_item[1]
                self.viewer.surface=self.surface
                got_surface=True
        if not got_surface: self.after(1000, self.check_generation)
        else: self.post_generation()
            #self.viewer.image_label.configure(text="HELLO")#, image=ImageTk.PhotoImage(Image.open(TMP_IMAGE_LOCATION)))

    def post_generation(self):
        self.surface.write_to_png(TMP_IMAGE_LOCATION)
        self.img=ImageTk.PhotoImage(Image.open(TMP_IMAGE_LOCATION).resize((300, 300), Image.ANTIALIAS))
        self.generate_button.configure(state=tk.NORMAL)
        self.viewer.image_label.configure(text="HAWDHALWKh", image=self.img)
        generator_running=False

def main():
    root=tk.Tk()
    app=PyWallpaper(root)
    app.grid()
    root.mainloop()

if __name__=='__main__':
    main()
