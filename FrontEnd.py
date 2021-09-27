import sys
from PySide6 import QtCore, QtWidgets, QtGui
from BlurWindow.blurWindow import GlobalBlur


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Title Bar in Pysiide6
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.setWindowTitle("ExifotocopyPlus")
        self.setFont(QtGui.QFont("Helvetica", 12))
        self.setAutoFillBackground(True)
        # Style
        # self.setWindowOpacity(20)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TintedBackground)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        GlobalBlur(int(self.winId()), hexColor=False, Acrylic=False, Dark=True, QWidget=self)
        self.setStyleSheet(
            "QMainWindow{ background: rgba(255 ,136, 26, 150) }"
            "QLineEdit { background-color: rgba(0,0, 0, 100) }"
            "QComboBox{ background-color: rgba(0,0, 0, 100) }"
            "QPushButton { background-color: rgba(0 ,0, 0, 0) }"
            "QLabel { color: white }"
            "QStatusBar{ background-color: rgba(255 ,136, 26, 150) }"
            "color:white"
            "background-color:rgba(10,10, 10, 10)")

        button = QtWidgets.QPushButton(self)
        button.setWindowOpacity(0.1)
        button.setIcon(QtGui.QIcon('images/icons/folder-received-fill.svg'))
        button.setIconSize(QtCore.QSize(24, 24))
        button.setStyleSheet("background-color:rgba(10,10, 10, 10)")

        sourceEntry = QtWidgets.QLineEdit("Source Folder", self)
        sourceLabel = QtWidgets.QLabel("Source Folder")

        destinationEntry = QtWidgets.QLineEdit(self)
        destinationLabel = QtWidgets.QLabel("Destination Folder")
        destinationButton = QtWidgets.QPushButton(self)
        destinationButton.setIcon(QtGui.QIcon('images/icons/folder-shared-fill.svg'))
        destinationButton.setIconSize(QtCore.QSize(24, 24))
        destinationButton.setStyleSheet("background-color:rgba(10,10, 10, 10)")

        fileExtensionEntry = QtWidgets.QLineEdit(self)
        fileExtensionLabel = QtWidgets.QLabel("Filename Extensions")

        datePolictBox = QtWidgets.QComboBox(self)
        datePolictLabel = QtWidgets.QLabel("No Exif Date Policity")

        sourceEntry.setStyleSheet('color:white')

        # Layout Settings
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(10)
        layout.addWidget(sourceLabel, 0, 0)
        layout.addWidget(sourceEntry, 0, 1)
        layout.addWidget(button, 0, 2)

        layout.addWidget(destinationLabel, 1, 0)
        layout.addWidget(destinationEntry, 1, 1)
        layout.addWidget(destinationButton, 1, 2)

        layout.addWidget(fileExtensionLabel, 2, 0)
        layout.addWidget(fileExtensionEntry, 2, 1)

        layout.addWidget(datePolictLabel, 3, 0)
        layout.addWidget(datePolictBox, 3, 1)

        depthOfFolderStructureLabel = QtWidgets.QLabel("Depth of Folder Structure")
        depthOfFolderStructureBox = QtWidgets.QComboBox()
        layout.addWidget(depthOfFolderStructureLabel,4,0)
        layout.addWidget(depthOfFolderStructureBox,4,1)

        button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
