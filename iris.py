import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog


class MainApplication(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.show()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction('&Open...', self.openFile)
        fileMenu.addAction('&Open directory...', self.openDirectory)

    def openFile(self):
        fitsExts = "All files (*) ;; Fits files (*.fts *.FTS *.fit *.FIT *.fits *.FITS)"
        files = QFileDialog.getOpenFileNames(parent=self,
                                             caption="Open file...",
                                             filter=fitsExts)
        print(files[0])

    def openDirectory(self):
        dirPath = QFileDialog.getExistingDirectory(parent=self,
                                                   caption="Open directory...")
        print(dirPath)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainApplication()
    sys.exit(app.exec_())
