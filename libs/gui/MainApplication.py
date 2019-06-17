from ..filesystem import ListOfFiles
from .WorkDirBrowser import WorkDirBrowser
from PyQt5 import QtWidgets


class MainApplication(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("IRIS")
        self.setGeometry(200, 200, 1024, 768)

        # Create menu bar with actions
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction('&Open...', self.open_file)
        file_menu.addAction('&Open directory...', self.open_directory)
        self.show()

    def open_file(self):

        # List of all possible fits-file extensions
        fits_extensions = "All files (*) ;; Fits files (*.fts *.FTS *.fit *.FIT *.fits *.FITS)"

        # List of opened files
        files = QtWidgets.QFileDialog.getOpenFileNames(parent=self,
                                                       caption="Open file...",
                                                       filter=fits_extensions)

    def open_directory(self):

        # Path to opened directory
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(parent=self,
                                                              caption="Open directory...")

        # Start work dir browser window if user choose a directiry
        if dir_path:
            self.work_dir_browser = WorkDirBrowser(self, ListOfFiles(dir_path))
