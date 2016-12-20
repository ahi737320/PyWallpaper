#!/usr/bin/env python3
#Python script that generates wallpapers
import tkinter as tk
import tkinter.ttk as ttk
import importlib
from algorithms.PaperAlgorithms import Circles
from algorithms.Helpers import *
importlib.reload(PaperAlgorithms)
#importlib.reload(Helpers)
from threading import Thread
from queue import Queue

generators={'Circles':0, 'Triangles':1}
generator_running=False

def run_generator(gen_type, queue, arguments):
    gen_thread=Thread(target=Circles, args=arguments+[queue])
    gen_thread.run()
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
        run_generator("Circles", self.queue, [(1920, 1080)])
        self.after(1000, self.check_generation)

    def check_generation(self):
        got_surface=False
        while not self.queue.empty():
            new_item=self.queue.get()
            self.queue.task_done
            if new_item[0]==0: self.percentage.set(new_item[1])
            elif new_item[0]==1:
                self.surface=new_item[1]
                got_surface=True
        if not got_surface: self.after(1000, self.check_generation)

def main():
    root=tk.Tk()
    app=PyWallpaper(root)
    app.grid()
    root.mainloop()

if __name__=='__main__':
    main()
