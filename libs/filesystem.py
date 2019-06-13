from os import listdir


class ListOfFiles(object):
    def __init__(self, dir_path):
        self.file_paths = listdir(dir_path)
        print(self.file_paths)
