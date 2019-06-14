from astropy.io import fits
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=3, height=3, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.ax.set_xticks([])
        self.ax.set_xticks([])

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        # Creating resizable FigureCanvas
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    @QtCore.pyqtSlot()
    def plot(self, selectedIndex=None):
        """Plot selected fits file"""
        path_to_fits = selectedIndex[0].data(role=QtCore.Qt.UserRole)  # Path to file
        image_data = fits.getdata(path_to_fits, ext=0)  # Get data from fits file

        # Plot data in PlotCanvas window
        self.ax.clear()
        self.ax.imshow(image_data, cmap='gray')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        plt.tight_layout()
        self.draw()
