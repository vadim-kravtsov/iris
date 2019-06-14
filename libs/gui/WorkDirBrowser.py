from ..graphics import PlotCanvas
from fnmatch import fnmatch
from PyQt5 import QtCore, QtWidgets, QtGui


class WorkDirBrowser(QtWidgets.QWidget):
    '''Window in which user can mark files as bias, dark, flat, etc.'''
    def __init__(self, parent, listOfFiles):
        super().__init__(parent=parent)

        # Set window properties
        self.setWindowFlags(QtCore.Qt.Window)
        self.setGeometry(350, 350, 800, 600)

        # Create containers
        self.hbox = QtWidgets.QHBoxLayout()
        self.vbox_left = QtWidgets.QVBoxLayout()
        self.vbox_right = QtWidgets.QVBoxLayout()

        # Create and fill model
        self.list_model = QtGui.QStandardItemModel()
        self.list_model.appendColumn(listOfFiles.qt_filelist)

        # Create files list widgets
        self.file_list = QtWidgets.QListView()
        self.file_list.setModel(self.list_model)  # Set model as list_model
        self.file_list.setWrapping(False)  # No line breaks
        self.file_list.setSelectionMode(3)  # Set extended selection
        self.file_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Disable editing

        # Create title
        self.file_list_label = QtWidgets.QLabel("Untagged files:", parent=self)
        self.file_list_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create search line
        self.file_list_text_field = QtWidgets.QLineEdit(parent=self)
        self.file_list_text_field.setCompleter(QtWidgets.QCompleter(listOfFiles.file_names, parent=self))
        self.file_list_text_field.setPlaceholderText("Enter file mask...")

        def search_by_mask(self, mask):
            """Set as visible only file names which match the mask"""
            file_names = listOfFiles.file_names
            if mask:
                indxs = [file_names.index(x) for x in file_names if fnmatch(x, mask)]
                for i in range(len(file_names)):
                    if i in indxs:
                        self.file_list.setRowHidden(i, False)
                    else:
                        self.file_list.setRowHidden(i, True)
            else:
                for i in range(len(file_names)):
                    self.file_list.setRowHidden(i, False)

        # Showing fits file, choosed by mouseclick or by pressing "Return"
        self.file_list.activated.connect(lambda: self.plot_canvas.plot(self.file_list.selectedIndexes()))

        # Hiding file names as don't match the mask
        self.file_list_text_field.textChanged.connect(lambda: search_by_mask(self, self.file_list_text_field.text()))

        self.plot_canvas = PlotCanvas()
        self.file_list3 = QtWidgets.QListView()

        self.file_list3.setModel(self.list_model)

        # Packaging widgets in containers
        self.vbox_left.addWidget(self.file_list_label)
        self.vbox_left.addWidget(self.file_list_text_field)
        self.vbox_left.addWidget(self.file_list)
        self.hbox.addLayout(self.vbox_left)
        self.vbox_right.addWidget(self.plot_canvas)
        self.vbox_right.addWidget(self.file_list3)
        self.hbox.addLayout(self.vbox_right)
        self.setLayout(self.hbox)
        self.show()
