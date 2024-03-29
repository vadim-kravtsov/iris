from ..graphics import PlotCanvas
from fnmatch import fnmatch
from ..filesystem import Settings
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
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        # Read settings
        self.settings = Settings()
        # Create containers
        self.main_vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.vbox_left = QtWidgets.QVBoxLayout()
        self.vbox_right = QtWidgets.QVBoxLayout()
        self.central_buttons = QtWidgets.QVBoxLayout()
        self.footer = QtWidgets.QHBoxLayout()

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

        # Create titles
        self.untagged_file_list_label = QtWidgets.QLabel("Untagged files:", parent=self)
        self.untagged_file_list_label.setAlignment(QtCore.Qt.AlignCenter)

        self.tabs_with_tagged_label = QtWidgets.QLabel("Tagged files:", parent=self)
        self.tabs_with_tagged_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create search line
        self.untagged_file_list_text_field = QtWidgets.QLineEdit(parent=self)
        self.untagged_file_list_text_field.setPlaceholderText("Enter file mask...")

        # Create plot canvas
        self.plot_canvas = PlotCanvas()

        # Create tab widget to show tagged_file_list as tabs
        self.tabs_with_tagged = QtWidgets.QTabWidget()
        self.tabs_with_tagged.file_tags = self.settings.file_tags
        self.tabs_with_tagged.setUsesScrollButtons(False)
        for tab_index in range(len(self.tabs_with_tagged.file_tags)):
            self.tabs_with_tagged.addTab(QtWidgets.QListView(), self.tabs_with_tagged.file_tags[tab_index])
            self.tabs_with_tagged.widget(tab_index).setModel(QtGui.QStandardItemModel())
            self.tabs_with_tagged.widget(tab_index).setSelectionMode(3)
            self.tabs_with_tagged.widget(tab_index).setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Create "autotag" button
        self.autotag_button = QtWidgets.QPushButton(parent=self)
        self.autotag_button.setText('A')
        self.autotag_button.setMaximumWidth(50)

        # Create "move as..." button
        self.move_button = QtWidgets.QPushButton(parent=self)
        self.move_button.setMaximumWidth(50)
        self.move_button.setText("M")
        self.move_button_menu = QtWidgets.QMenu()
        self.move_button.setMenu(self.move_button_menu)
        for file_tag in self.tabs_with_tagged.file_tags:
            self.move_button_menu.addAction(file_tag, lambda x=file_tag: self.tag_files_as(x))  #x=file_tag is important

        # Fill footer
        self.ok_button = QtWidgets.QPushButton(parent=self)
        self.ok_button.setText("Ok")
        self.cancel_button = QtWidgets.QPushButton(parent=self)
        self.cancel_button.setText("Cancel")
        self.ok_button.setMaximumWidth(100)
        self.cancel_button.setMaximumWidth(100)
        self.footer.addStretch()
        self.footer.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignLeft)
        self.footer.addWidget(self.ok_button, alignment=QtCore.Qt.AlignRight)
        
        # Packaging widgets in containers
        self.vbox_left.addWidget(self.untagged_file_list_label)
        self.vbox_left.addWidget(self.untagged_file_list_text_field)
        self.vbox_left.addWidget(self.untagged_file_list)
        self.hbox.addLayout(self.vbox_left)
        self.central_buttons.addStretch()
        self.central_buttons.addWidget(self.autotag_button, alignment=QtCore.Qt.AlignCenter)
        self.central_buttons.addWidget(self.move_button, alignment=QtCore.Qt.AlignCenter)
        self.central_buttons.addStretch()
        self.hbox.addLayout(self.central_buttons)
        self.vbox_right.addWidget(self.plot_canvas)
        self.vbox_right.addWidget(self.tabs_with_tagged_label)
        self.vbox_right.addWidget(self.tabs_with_tagged)
        self.hbox.addLayout(self.vbox_right)
        self.main_vbox.addLayout(self.hbox)
        self.main_vbox.addLayout(self.footer)
        self.setLayout(self.main_vbox)
        self.show()

    def set_behavior(self):
        # Showing fits file, choosed by mouseclick or by pressing "Return"
        self.untagged_file_list.activated.connect(lambda: self.plot_canvas.plot(self.untagged_file_list.currentIndex()))
    
        # Hiding file names as don't match the mask
        self.untagged_file_list_text_field.textChanged.connect(lambda: self.search_by_mask(self.untagged_file_list_text_field.text()))

        self.cancel_button.clicked.connect(self.close)
        self.autotag_button.clicked.connect(self.autotag_files)

    @QtCore.pyqtSlot()
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

    @QtCore.pyqtSlot()
    def tag_files_as(self, label):
        """Function for tagging files as dark, bias, flat, etc."""
        selected_items = [self.untagged_list_model.itemFromIndex(x) for x in self.untagged_file_list.selectedIndexes()]
        tab_index = self.tabs_with_tagged.file_tags.index(label)
        for item in selected_items:
            self.untagged_list_model.setData(item.index(), label, role=QtCore.Qt.UserRole+1)
            self.untagged_list_model.takeRow(item.row())
            self.tabs_with_tagged.widget(tab_index).model().appendRow(item)
        self.untagged_file_list.clearSelection()
        self.tabs_with_tagged.setCurrentIndex(tab_index)

    @QtCore.pyqtSlot()
    def autotag_files(self):
        masks = self.settings.file_masks
        for tag in self.settings.file_tags:
            mask = masks[tag]
            if mask:
                mask = '*' + mask + '*'
                tab_index = self.tabs_with_tagged.file_tags.index(tag)
                file_names = []
                for row in range(self.untagged_list_model.rowCount()):
                    file_names.append(self.untagged_list_model.item(row).text())
                indxs = [file_names.index(x) for x in file_names if fnmatch(x, mask)]
                items = [self.untagged_list_model.item(i) for i in indxs]
                for item in items:
                    if item:
                        self.untagged_list_model.setData(item.index(), tag, role=QtCore.Qt.UserRole+1)
                        self.untagged_list_model.takeRow(item.row())
                        self.tabs_with_tagged.widget(tab_index).model().appendRow(item)
