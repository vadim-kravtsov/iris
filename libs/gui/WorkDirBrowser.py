from ..graphics import PlotCanvas
from PyQt5 import QtCore, QtWidgets, QtGui


class WorkDirBrowser(QtWidgets.QWidget):
    '''Window in which user can mark files as bias, dark, flat, etc.'''
    def __init__(self, parent, ListOfFiles):
        super().__init__(parent=parent)

        # Set window properties
        self.setWindowFlags(QtCore.Qt.Window)
        self.setGeometry(350, 350, 800, 600)

        # Create containers
        self.hbox = QtWidgets.QHBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()

        # Create and fill model
        self.list_model = QtGui.QStandardItemModel()
        self.list_model.appendColumn([QtGui.QStandardItem(x) for x in ListOfFiles.file_names])

        # Addind paths in model as data with role=UserRole
        i = 0
        for path in ListOfFiles.file_paths:
            self.list_model.setData(self.list_model.index(i, 0), path, role=QtCore.Qt.UserRole)
            i += 1

        # Customizing widgets
        self.file_list = QtWidgets.QListView()
        self.file_list.setModel(self.list_model)  # Set model as list_model
        self.file_list.setWrapping(False)  # No line breaks
        self.file_list.setSelectionMode(3)  # Set extended selection
        self.file_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Disable editing

        self.plot_canvas = PlotCanvas()
        self.file_list3 = QtWidgets.QListView()

        # Associating choosing element from file_list with plot function
        self.file_list.activated.connect(lambda: self.plot_canvas.plot(self.file_list.selectedIndexes()))

        self.file_list3.setModel(self.list_model)

        # Packaging widgets in containers
        self.hbox.addWidget(self.file_list)
        self.vbox.addWidget(self.plot_canvas)
        self.vbox.addWidget(self.file_list3)
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)
        self.show()
