from .graphics import PlotCanvas
from PyQt5 import QtCore, QtWidgets


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
        self.list_model = QtCore.QStringListModel(ListOfFiles.file_paths)

        # Customizing widgets
        self.file_list = QtWidgets.QListView()
        self.file_list.setWrapping(False)  # No line breaks
        self.file_list.setSelectionMode(3)  # Set extended selection
        self.file_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Disable editing
        self.file_list.setModel(self.list_model)

        self.file_list2 = PlotCanvas()
        self.file_list3 = QtWidgets.QListView()
        self.file_list3.setModel(self.list_model)

        # Packaging widgets in containers
        self.hbox.addWidget(self.file_list)
        self.vbox.addWidget(self.file_list2)
        self.vbox.addWidget(self.file_list3)
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)
        self.show()
