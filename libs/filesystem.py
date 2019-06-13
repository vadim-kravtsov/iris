from pathlib import Path


class ListOfFiles(object):
    def __init__(self, dir_path):
        self.file_paths = list(Path(dir_path).glob('*.*'))
        self.file_names = [p.parts[-1] for p in self.file_paths]
