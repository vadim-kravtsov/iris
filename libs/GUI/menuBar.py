import tkinter as Tk
from tkinter import filedialog
from .toolsWindows import DirBrowser
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
        self.filenames = filedialog.askopenfilenames(parent=self.window.root,
                                                     title="Choose a file",
                                                     filetypes=(("fits files", fileSystem.fitsExts),
                                                                ("all files", "*.*")))
        if self.filenames:
            print(self.filenames)

    def open_dir(self):
        self.pathToDir = filedialog.askdirectory(parent=self.window.root,
                                                 title="Choose a directory")
        if self.pathToDir:
            self.window.dirbrowser = DirBrowser(self.window, self.pathToDir)
