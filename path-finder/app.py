import importlib
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

"""
class MainWindowForm(QWidget):
    def __init__(self):
        super().__init__()
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Cost: ", QLineEdit())
        self.form_layout.addRow("Distance: ", QLineEdit())

        self.submit_button = QPushButton("OK")

        self.setLayout(self.form_layout)
"""


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
        #self.parent.on_update_mode(selected_mode)

        
class MainWindow(QMainWindow):
    def __init__(self, osi, modes):
        super().__init__()
        self.modes = modes
        self.mode = None
        self.osi = osi
        self.mode = 0
        #set window icons/logos
        self.setWindowTitle(self.osi.GetTitle())
        self.setMinimumSize(QSize(self.osi.GetHeight(), self.osi.GetWidth()))

        #initialize layouts
        self.main_layout = QVBoxLayout()
        self.main_menu_layout = MainWindowMenu(self, self.osi)
        self.main_layout.addWidget(self.main_menu_layout)

        #set empty widget
        self.widget = QWidget()
        self.on_update_mode(self.modes[0])

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
    empty_grid_class = getattr(importlib.import_module("widgets.empty_widget"), "EmptyWidget")
    xy_window_class = getattr(importlib.import_module("widgets.xy_grid"), "XYWindow")

    modes = [
        {"active": False, "index": 0, "name": "None Selected", "widget": empty_grid_class},
        {"active": True, "index": 1, "name": "2D Pathfinder", "widget": xy_window_class},
        {"active": True, "index": 2, "name": "3D Pathfinder"}
    ]
    window = MainWindow(osi, modes)
    window.show()
    sys.exit(app.exec())
