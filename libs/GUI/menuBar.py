import tkinter as Tk
from tkinter import filedialog
from .. import fileSystem


class MenuBar(Tk.Frame):
    def __init__(self, window):
        self.window = window
        self.menubar = Tk.Menu(self.window.root)
        self.filemenu = Tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open...", command=self.open_file)
        self.filemenu.add_command(label="Open directory...",
                                  command=self.open_dir)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

    def open_file(self):
        self.filename = filedialog.askopenfilename(parent=self.window.root,
                                                   title="Choose a file", )
        print(self.filename)

    def open_dir(self):
        self.filenames = filedialog.askopenfilenames(parent=self.window.root,
                                                     title="Choose a files", )
        print(self.filenames)
