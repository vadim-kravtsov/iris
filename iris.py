<<<<<<< HEAD
import sys
from PyQt5.QtWidgets import QApplication
from libs.gui.MainApplication import MainApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainApplication()
    sys.exit(app.exec_())
=======
#!/usr/bin/env python

from libs.MainApplication import MainApplication


def main():
    MainApplication()


if __name__ == '__main__':
    main()
>>>>>>> b8ebc379be3b99b923dfeb42d53a80a8eba0b04c
