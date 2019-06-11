import tkinter as Tk


def donothing():
    x = 0


class MenuBar(Tk.Frame):
    def __init__(self, window):
        self.window = window
        self.menubar = Tk.Menu(self.window.root)
        self.filemenu = Tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open...", command=donothing)
        self.filemenu.add_command(label="Open directory...", command=donothing)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
