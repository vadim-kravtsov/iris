from ..graphics import PlotCanvas
from fnmatch import fnmatch
from PyQt5 import QtCore, QtWidgets, QtGui


class WorkDirBrowser(QtWidgets.QWidget):
    '''Window in which user can mark files as bias, dark, flat, etc.'''
    def __init__(self, parent, listOfFiles):
        super().__init__(parent=parent)
        self.initUI(listOfFiles)
        self.set_behavior()

    def initUI(self, listOfFiles):
        # Set window properties
        self.setWindowFlags(QtCore.Qt.Window)
        self.setGeometry(350, 350, 800, 600)
        self.setWindowTitle(str(listOfFiles.base_path))

        # Create containers
        self.hbox = QtWidgets.QHBoxLayout()
        self.vbox_left = QtWidgets.QVBoxLayout()
        self.vbox_right = QtWidgets.QVBoxLayout()
        self.central_buttons = QtWidgets.QVBoxLayout()

        # Create and fill model
        self.untagged_list_model = QtGui.QStandardItemModel()
        self.untagged_list_model.appendColumn(listOfFiles.qt_filelist)
        self.untagged_list_model.sort(0)

        # Create list view widget for viewing untagged files
        self.untagged_file_list = QtWidgets.QListView()
        self.untagged_file_list.setModel(self.untagged_list_model)  # Set model as untagged_list_model
        self.untagged_file_list.setWrapping(False)  # No line breaks
        self.untagged_file_list.setSelectionMode(3)  # Set extended selection
        self.untagged_file_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Disable editing

        # Create title
        self.untagged_file_list_label = QtWidgets.QLabel("Untagged files:", parent=self)
        self.untagged_file_list_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create search line
        self.untagged_file_list_text_field = QtWidgets.QLineEdit(parent=self)
        self.untagged_file_list_text_field.setPlaceholderText("Enter file mask...")

        # Create plot canvas
        self.plot_canvas = PlotCanvas()

        # Create and customize list view widget for viewing tagged files
       
        # Create tab widget to show tagged_file_list as tabs
        self.tabs_with_tagged = QtWidgets.QTabWidget()
        self.tabs_with_tagged.file_types = ['object', 'darks', 'biases', 'flats', 'fringes']
       
        for i in range(len(self.tabs_with_tagged.file_types)):
            self.tabs_with_tagged.addTab(QtWidgets.QListView(), self.tabs_with_tagged.file_types[i])
            self.tabs_with_tagged.widget(i).setModel(QtGui.QStandardItemModel())
            self.tabs_with_tagged.widget(i).setSelectionMode(3)

        # Create "add" button
        self.add_button = QtWidgets.QPushButton(parent=self)
        self.add_button.setText('A')
        self.add_button.setMaximumWidth(50)

        # Create "move as..." button
        self.move_button = QtWidgets.QPushButton(parent=self)
        self.move_button.setMaximumWidth(50)
        self.move_button.setText("M")
        self.move_button_menu = QtWidgets.QMenu()
        self.move_button_menu.addAction("Object", lambda: self.mark_files_as('object'))
        self.move_button_menu.addAction("Dark", lambda: self.mark_files_as('darks'))
        self.move_button_menu.addAction("Bias", lambda: self.mark_files_as('biases'))
        self.move_button_menu.addAction("Flat", lambda: self.mark_files_as('flats'))
        self.move_button_menu.addAction("Fringe", lambda: self.mark_files_as('fringes'))
        self.move_button.setMenu(self.move_button_menu)

        # Packaging widgets in containers
        self.vbox_left.addWidget(self.untagged_file_list_label)
        self.vbox_left.addWidget(self.untagged_file_list_text_field)
        self.vbox_left.addWidget(self.untagged_file_list)
        self.hbox.addLayout(self.vbox_left)
        self.central_buttons.addWidget(self.add_button)
        self.central_buttons.addWidget(self.move_button)
        self.hbox.addLayout(self.central_buttons)
        self.vbox_right.addWidget(self.plot_canvas)
        self.vbox_right.addWidget(self.tabs_with_tagged)
        self.hbox.addLayout(self.vbox_right)
        self.setLayout(self.hbox)
        self.show()

    def set_behavior(self):
        # Showing fits file, choosed by mouseclick or by pressing "Return"
        self.untagged_file_list.activated.connect(lambda: self.plot_canvas.plot(self.untagged_file_list.selectedIndexes()))

        # Hiding file names as don't match the mask
        self.untagged_file_list_text_field.textChanged.connect(lambda: self.search_by_mask(self.untagged_file_list_text_field.text()))

    def search_by_mask(self, mask):
        """Set as visible only file names which match the mask"""
        file_names = []
        for row in range(self.untagged_list_model.rowCount()):
            file_names.append(self.untagged_list_model.item(row).text())
        if mask:
            mask = '*' + mask + '*'
            indxs = [file_names.index(x) for x in file_names if fnmatch(x, mask)]
            for i in range(len(file_names)):
                if i in indxs:
                    self.untagged_file_list.setRowHidden(i, False)
                else:
                    self.untagged_file_list.setRowHidden(i, True)
            self.untagged_list_model.sort(0)
        else:
            for i in range(len(file_names)):
                self.untagged_file_list.setRowHidden(i, False)
            self.untagged_list_model.sort(0)

    def mark_files_as(self, label):
        """Function for tagging files as dark, bias, flat, etc."""
        selected_items = [self.untagged_list_model.itemFromIndex(x) for x in self.untagged_file_list.selectedIndexes()]
        tab_index = self.tabs_with_tagged.file_types.index(label)
        for item in selected_items:
            self.untagged_list_model.setData(item.index(), label, role=QtCore.Qt.UserRole+1)
            self.untagged_list_model.takeRow(item.row())
            self.tabs_with_tagged.widget(tab_index).model().appendRow(item)
        self.untagged_file_list.clearSelection()
        
