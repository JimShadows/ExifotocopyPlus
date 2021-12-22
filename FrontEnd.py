import sys
from PySide6 import QtCore, QtWidgets, QtGui
from BlurWindow.blurWindow import GlobalBlur


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.source = ''

        self.init_ui()
        self.magic()

    def init_ui(self):
        # Title Bar in Pysiide6
        self.setWindowIcon(QtGui.QIcon('images/images/logo.png'))
        self.setWindowTitle("ExifotocopyPlus")
        self.setFont(QtGui.QFont("Helvetica", 12))
        self.setAutoFillBackground(True)
        # Style
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        self.setAttribute(QtCore.Qt.WA_TintedBackground, False)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # GlobalBlur(int(self.winId()), hexColor=False, Acrylic=False, Dark=True, QWidget=self)
        self.setStyleSheet(
            "QMainWindow { background-color: rgba(43 ,43, 43, 200) }"
            "QToolTip {opacity:200}"
            "QMenu {background-color:red}"
            "QMenuBar{background-color: rgba(0 ,0, 0, 100)}"
            "QLineEdit { background-color: rgba(26,26, 26, 100) }"
            "QLineEdit { color: silver }"
            "QLineEdit { border-width: 1px}"
            "QLineEdit { border-style: ridge}"
            "QLineEdit { border-color: rgba(0,0,0,50)}"
            "QLineEdit { outline-color: rgb(55,200, 113) }"
            "QComboBox{ background-color: rgba(26,26, 26, 100) }"
            "QPushButton { background-color: rgba(0 ,0, 0, 0) }"
            "QLabel { color: silver }"
            "QStatusBar{ background-color: rgba(255 ,136, 26, 150) }")

        button = QtWidgets.QPushButton(self)
        button.setWindowOpacity(0.1)
        button.setIcon(QtGui.QIcon('images/icons/folder-received-fill.svg'))
        button.setIconSize(QtCore.QSize(24, 24))
        button.setStyleSheet("background-color:rgba(10,10, 10, 10)")

        source_entry = QtWidgets.QLineEdit(self.source, self)
        source_label = QtWidgets.QLabel("Source Folder")

        destination_entry = QtWidgets.QLineEdit(self)
        destinationLabel = QtWidgets.QLabel("Destination Folder")
        destinationButton = QtWidgets.QPushButton(self)
        destinationButton.setWindowOpacity(0.1)
        destinationButton.setIcon(QtGui.QIcon('images/icons/folder-shared-fill.svg'))
        destinationButton.setIconSize(QtCore.QSize(24, 24))
        destinationButton.setStyleSheet("background-color:rgba(10,10, 10, 10)")

        fileExtensionEntry = QtWidgets.QLineEdit(self)
        fileExtensionLabel = QtWidgets.QLabel("Filename Extensions")
        fileExtensionButton = QtWidgets.QPushButton(self)
        fileExtensionButton.setWindowOpacity(0.1)
        fileExtensionButton.setIcon(QtGui.QIcon('images/icons/file-settings-line.svg'))
        fileExtensionButton.setIconSize(QtCore.QSize(24, 24))
        fileExtensionButton.setStyleSheet("background-color:rgba(10,10, 10, 10)")

        datePolictBox = QtWidgets.QComboBox(self)
        datePolictLabel = QtWidgets.QLabel("No Exif Date Policity")

        '''Layout Settings'''
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(10)
        layout.addWidget(source_label, 0, 0)
        layout.addWidget(source_entry, 0, 1)
        layout.addWidget(button, 0, 2)

        layout.addWidget(destinationLabel, 1, 0)
        layout.addWidget(destination_entry, 1, 1)
        layout.addWidget(destinationButton, 1, 2)

        layout.addWidget(fileExtensionLabel, 2, 0)
        layout.addWidget(fileExtensionEntry, 2, 1)
        layout.addWidget(fileExtensionButton, 2, 2)

        layout.addWidget(datePolictLabel, 3, 0)
        layout.addWidget(datePolictBox, 3, 1)

        depthOfFolderStructureLabel = QtWidgets.QLabel("Depth of Folder Structure")
        depthOfFolderStructureBox = QtWidgets.QComboBox()
        layout.addWidget(depthOfFolderStructureLabel, 4, 0)
        layout.addWidget(depthOfFolderStructureBox, 4, 1)

        formatStringLevel1Folder = QtWidgets.QLabel

        button.clicked.connect(self.magic)
        destinationButton.clicked.connect(self.destination)

    @QtCore.Slot()
    def magic(self):
        file = QtWidgets.QFileDialog.getExistingDirectory()
        self.source = str(file)

    @QtCore.Slot()
    def destination(self):
        QtWidgets.QFileDialog.getExistingDirectory()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
