import sys
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.source = ''

        self.init_ui()

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
            "QMainWindow { background-color: rgb(43 ,43, 43) }"
            "QToolTip {opacity:200}"
            "QMenu {background-color:red}"
            "QMenuBar{background-color: rgb(0 ,0, 0)}"
            "QLineEdit { background-color: rgb(26,26, 26) }"
            "QLineEdit { color: silver }"
            "QLineEdit { border-width: 1px}"
            "QLineEdit { border-style: ridge}"
            "QLineEdit { border-color: rgb(0,0,0)}"
            "QLineEdit { outline-color: rgb(55,200, 113) }"
            "QComboBox{ background-color: rgb(26,26, 26) }"
            "QPushButton { background-color: rgba(0 ,0, 0, 0) }"
            "QLabel { color: silver }"
            "QStatusBar{ background-color: rgba(255 ,136, 26, 150) }")

        source_button = QtWidgets.QPushButton(self)
        source_button.setWindowOpacity(0.1)
        source_button.setIconSize(QtCore.QSize(24, 24))
        source_button.setStyleSheet("background-color:rgb(10,10, 10)")
        source_button.setIcon(QtGui.QIcon('images/icons/folder-received-fill.svg'))

        source_entry = QtWidgets.QLineEdit(self.source, self)
        source_label = QtWidgets.QLabel("Source Folder")

        destination_entry = QtWidgets.QLineEdit(self)
        destination_label = QtWidgets.QLabel("Destination Folder")

        destination_button = QtWidgets.QPushButton(self)
        destination_button.setWindowOpacity(0.1)
        destination_button.setIcon(QtGui.QIcon('images/icons/folder-shared-fill.svg'))
        destination_button.setIconSize(QtCore.QSize(24, 24))
        destination_button.setStyleSheet("background-color:rgb(10,10, 10)")

        file_extension_entry = QtWidgets.QLineEdit(self)
        file_extension_label = QtWidgets.QLabel("Filename Extensions")
        file_extension_button = QtWidgets.QPushButton(self)
        file_extension_button.setWindowOpacity(0.1)
        file_extension_button.setIcon(QtGui.QIcon('images/icons/file-settings-line.svg'))
        file_extension_button.setIconSize(QtCore.QSize(24, 24))
        file_extension_button.setStyleSheet("background-color:rgb(10,10, 10)")

        date_policy_box = QtWidgets.QComboBox(self)
        date_policy_label = QtWidgets.QLabel("No Exif Date Policity")

        '''Layout Settings'''
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(10)
        layout.addWidget(source_label, 0, 0)
        layout.addWidget(source_entry, 0, 1)
        layout.addWidget(source_button, 0, 2)

        layout.addWidget(destination_label, 1, 0)
        layout.addWidget(destination_entry, 1, 1)
        layout.addWidget(destination_button, 1, 2)

        layout.addWidget(file_extension_label, 2, 0)
        layout.addWidget(file_extension_entry, 2, 1)
        layout.addWidget(file_extension_button, 2, 2)

        layout.addWidget(date_policy_label, 3, 0)
        layout.addWidget(date_policy_box, 3, 1)

        depth_of_folder_structure_label = QtWidgets.QLabel("Depth of Folder Structure")
        depth_of_folder_structure_box = QtWidgets.QComboBox()
        layout.addWidget(depth_of_folder_structure_label, 4, 0)
        layout.addWidget(depth_of_folder_structure_box, 4, 1)

        source_button.clicked.connect(self.magic)
        destination_button.clicked.connect(self.destination)

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
