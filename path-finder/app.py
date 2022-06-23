import sys

from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QGridLayout, QFormLayout, QLineEdit,
        QVBoxLayout, QHBoxLayout, QPushButton,
        QLabel, QComboBox

        )
from PyQt5.QtCore import QSize, Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from tools import OSInterface
from metadata import Modes

class MainWindowMenu(QWidget):
    selected_mode = pyqtSignal(int)
    def __init__(self, parent, osi):
        super().__init__(parent)
        self.parent = parent
        self.osi = osi
        self.menu_layout = QFormLayout()

        self.menu_img = QLabel()
        self.img_pixmap = QPixmap(self.osi.GetWindowsIcon())
        self.menu_img.setPixmap(
            self.img_pixmap.scaled(
                QSize(
                    int(self.menu_img.width()/4),
                    int(self.menu_img.height()/4)
                ),
                aspectRatioMode=Qt.KeepAspectRatio
            )
        )

        self.title_label = QLabel()
        self.title_label.setText(self.osi.GetTitle())
        self.title_label.setAlignment(Qt.AlignCenter)

        self.mode_label = QLabel()
        self.mode_label.setText("Selected Mode")
        self.mode_label.setAlignment(Qt.AlignCenter)

        self.mode_box = QComboBox()
        for mode in modes:
            self.mode_box.insertItem(mode.get("index"), mode.get("name"))
            self.mode_box.model().item(mode.get("index")).setEnabled(mode.get("active"))
        self.mode_box.currentIndexChanged.connect(slot=self.on_mode_valueChanged)

        self.menu_layout.addWidget(self.title_label)
        self.menu_layout.addWidget(self.menu_img)
        self.menu_layout.addWidget(self.mode_label)
        self.menu_layout.addWidget(self.mode_box)

        self.setLayout(self.menu_layout)

    
    @pyqtSlot(int)
    def on_mode_valueChanged(self, selected_mode: int):
        for mode in modes:
            if mode.get("index") == selected_mode:
                self.parent.on_update_mode(mode)

        
class MainWindow(QMainWindow):
    def __init__(self, osi):
        super().__init__()
        self.osi = osi
        self.mode = [None]
        #set window icons/logos
        self.setWindowTitle(self.osi.GetTitle())
        self.setMinimumSize(QSize(self.osi.GetHeight(), self.osi.GetWidth()))

        #initialize layouts
        self.main_layout = QVBoxLayout()
        self.main_menu_layout = MainWindowMenu(self, self.osi)
        self.main_layout.addWidget(self.main_menu_layout)

        #set empty widget
        self.widget = QWidget()
        self.on_update_mode(modes[0])

        #self.main_layout.addWidget(self.form_layout)

        #add layouts to QWidget and set as main widget for entire app
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def on_update_mode(self, selected_mode: dict):
        """ Called when mode is updated in MainMenuWindow"""
        if selected_mode.get("widget") is not None:
            self.main_layout.removeWidget(self.widget)
            self.widget.deleteLater()
            self.mode = selected_mode
            widget = self.mode.get("widget")
            self.widget = widget(parent=self)
            self.main_layout.addWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    osi = OSInterface()
    app.setWindowIcon(QIcon(osi.GetWindowsIcon()))
    #loading up instances of empty widgets to initialize when user select a mode
    modes = Modes().modes
    window = MainWindow(osi)
    window.show()
    sys.exit(app.exec())
