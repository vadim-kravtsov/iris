import tkinter as Tk


class DirBrowser(Tk.Frame):
    def __init__(self, window, dirPath):
        self.window = window
        self.dirbrowser = Tk.Toplevel()
        self.dirbrowser.geometry("600x500")
