from pathlib import Path
from PyQt5.QtGui import QStandardItem
from PyQt5 import QtCore


class ListOfFiles(object):
    def __init__(self, dir_path):
        self.file_paths = list(Path(dir_path).glob('*.*'))
        self.file_names = [p.parts[-1] for p in self.file_paths]
        self.qt_filelist = [QStandardItem(x) for x in self.file_names]
        for item in self.qt_filelist:
            item.setData(self.file_paths[self.qt_filelist.index(item)], role=QtCore.Qt.UserRole)
