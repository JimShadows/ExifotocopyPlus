import sys
from ctypes.wintypes import HWND

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from BlurWindow.blurWindow import GlobalBlur


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 400)

        GlobalBlur(self.winId(),hexColor=False,Acrylic=False,Dark=False,QWidget=self)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())