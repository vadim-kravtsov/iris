from astropy.io import fits
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from numpy import median, std

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=3, height=3, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        # Creating resizable FigureCanvas
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    @QtCore.pyqtSlot()
    def plot(self, selectedIndex=None):
        """Plot selected fits file"""
        path_to_file = selectedIndex.data(role=QtCore.Qt.UserRole)  # Path to file
        fits_file_extensions = ['.fit', '.FIT', '.fts', '.FTS', '.fits', '.FITS']
        if path_to_file.suffix in fits_file_extensions:
            image_data = fits.getdata(path_to_file, ext=0)  # Get data from fits file
            median_brightness = median(image_data)
            std_brightness = std(image_data)
            # Plot data in PlotCanvas window
            self.ax.clear()
            self.ax.imshow(image_data, cmap='gray',
                           vmin=median_brightness-2*std_brightness,
                           vmax=median_brightness+2*std_brightness)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            plt.tight_layout()
            self.draw()
