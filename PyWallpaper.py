#!/usr/bin/env python3
#Python script that generates wallpapers
import tkinter as tk
import tkinter.ttk as ttk

class Generator(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

class Viewer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

class PyWallpaper(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent=parent
        self.notebook=ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, columnspan=2)
        self.generate=tk.Button(self)
        self.generate.grid(row=1, column=0)
        self.percentage=ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.percentage.grid(row=1, column=1)
        self.generator=Generator(self.notebook)
        self.generator.grid(row=0, column=0)
        self.viewer=Viewer(self.notebook)
        self.viewer.grid(row=0, column=0)
        self.notebook.add(self.generator, text='One')
        self.notebook.add(self.viewer, text='Two')

def main():
    root=tk.Tk()
    PyWallpaper(root).pack()
    root.mainloop()

if __name__=='__main__':
    main()
