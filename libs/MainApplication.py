#!/usr/bin/env python

import tkinter as Tk
from tkinter import messagebox
from .GUI.menuBar import MenuBar


class MainApplication(object):
    def __init__(self):
        # Create root window
        # Create main window base frame
        self.root = Tk.Tk()
        self.root.option_add('*foreground', '#969696')

        # Configure root window
        self.root.title("IRIS")
        self.root.protocol('WM_DELETE_WINDOW', self.shutdown)
        self.root.geometry("800x600")
        self.root.config(menu=MenuBar(self).menubar)
        self.root.mainloop()

    def shutdown(self):
        """
        This function is called when the user hit close window button
        """
        self.root.destroy()  # while testing
        #answer = messagebox.askokcancel("Close", "Really close?")
        #if answer is True:
        #    self.alive = False
        #    # Close the main window
        #    self.root.destroy()
