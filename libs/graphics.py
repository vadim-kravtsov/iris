import random
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=3, height=3, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        self.ax.plot(data, 'r-')
        self.ax.set_title('PyQt Matplotlib Example')
        self.draw()
