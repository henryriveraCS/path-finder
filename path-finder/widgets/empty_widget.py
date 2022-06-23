from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPalette, QFont

from tools import Colors

class EmptyWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        #initialize layouts
        self.main_layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setText("Select a mode in the menu above to start.")
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("color:black;");

        self.main_layout.addWidget(self.label)
        self.setLayout(self.main_layout)
        

    def paintEvent(self, parent):
        qp = QPainter()
        qp.begin(self)
        #qp.setRenderHints(qp.Antialiasing)
        #set background color
        brush = QBrush(Colors.white)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width(), self.height())
        qp.end()
