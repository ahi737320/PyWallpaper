#!/usr/bin/env python3
#Python script that generates wallpapers
import tkinter as tk
import tkinter.ttk as ttk
#from Generators import *
from threading import Thread
from queue import Queue

generators={'Circles':0, 'Triangles':1}
def tester(a, b, c, d):
    print("HELO")

def run_generator(gen_type, queue, arguments):
    #if gen_type=='Circles':
    gen_thread=Thread(target=Circles, args=arguments+[queue])
    #gen_thread=Thread(target=tester, args=([1, 2, 3, 4]))
    gen_thread.run()
    print(queue.get(False))
    queue.task_done()


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
        self.generate_button=tk.Button(self, text="Generate Pattern", command=lambda: run_generator("Circles", self.queue, [(1920, 1080)]))
        self.generate_button.grid(row=1, column=0)
        self.percentage=ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.percentage.grid(row=1, column=1)
        self.generator=Generator(self.notebook)
        self.generator.grid(row=0, column=0)
        self.viewer=Viewer(self.notebook)
        self.viewer.grid(row=0, column=0)
        self.notebook.add(self.generator, text='Generator')
        self.notebook.add(self.viewer, text='Viewer')

def main():
    root=tk.Tk()
    a=PyWallpaper(root)
    a.grid()
    root.mainloop()

if __name__=='__main__':
    main()
