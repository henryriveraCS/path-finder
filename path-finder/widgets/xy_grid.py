import sys

from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QGridLayout, QFormLayout, QLineEdit,
        QVBoxLayout, QHBoxLayout, QPushButton,
        QLabel, QComboBox

        )
from PyQt5.QtCore import QSize, Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from tools import Colors
from algorithms import xy

class NodeWidget(QWidget, xy.Node):
    def __init__(self, parent, point, pos_x, pos_y, height, width):
        super(Node, self).__init__(parent, point, pos_x, pos_y, height, width)
        #node logic
        self.parent = parent
        self.point = point
        self.cost = 1 
        self.G = 0
        self.H = 0
        self.distance = float(math.inf)
        self.is_wall = False
        self.is_visited = False
        self.is_path = False

        #qt metadata
        self.background_color = Colors.white
        self.wall_color = Colors.blue
        self.start_color = Colors.dark_green
        self.path_color = Colors.dark_yellow
        self.goal_color = Colors.dark_red
        self.visited_color = Colors.dark_cyan
        self.height = height
        self.width = width
        self.pos_x = pos_x
        self.pos_y = pos_y

    def paintEvent(self, parent):
        qp = QPainter()
        qp.being(self)
        #qp.setRenderHints(qp.Antialiasing)
        if self.is_wall:
            brush = QBrush(self.wall_color)
            qp.setBrush(brush)
        elif self.is_start:
            brush = QBrush(self.start_color)
            qp.setBrush(brush)
        elif self.is_end:
            brush = QBrush(self.end_color)
            qp.setBrush(brush)
        elif self.is_visited:
            brush = QBrush(self.visited_color)
            qp.setBrush(brush)
        elif self.is_path:
            brush = QBrush(self.visited_color)
            qp.setBrush(brush)
        else:
            brush = QBrush(self.background_color)
            qp.setBrush(brush)

        qp.drawRect(0, 0, self.width, self.height)
        #qp.drawText(0, 0, str(self.point))
        qp.end()

    def move_cost(self):
        return self.cost


class GridForm(QWidget):
    def __init__(self):
        super().__init__()
        self.form_layout = QFormLayout()

        
        self.title_label = QLabel()
        self.title_label.setText("2D Search Menu")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.algo_label = QLabel()
        self.algo_label.setText("Selected search algorithm")
        self.algo_label.setAlignment(Qt.AlignCenter)

        self.algo_box = QComboBox()
        self.algo_box.insertItem(0, "None selected")
        self.algo_box.insertItem(1, "Astar algorithm")
        self.algo_box.insertItem(2, "Djikstra algorithm")
        self.algo_box.model().item(0).setEnabled(False)
        #set here

        self.time_box = QComboBox()
        self.time_box.insertItem(0, "Instant")
        self.time_box.insertItem(1, "1 step per second")
        self.time_box.insertItem(2, "2 step per second")
        self.time_box.insertItem(3, "3 step per second")


        self.rows = 5
        self.cols = 5
        self.row_label = QLabel()
        self.row_label.setText("Rows:")
        self.row_label.setAlignment(Qt.AlignCenter)
        self.row_line = QLineEdit()
        self.row_line.setText(str(self.cols))

        self.col_label = QLabel()
        self.col_label.setText("Columns:")
        self.col_label.setAlignment(Qt.AlignCenter)
        self.col_line = QLineEdit()
        self.col_line.setText(str(self.rows))

        self.direction_label = QLabel()
        self.direction_label.setText("Direction:")
        self.direction_label.setAlignment(Qt.AlignCenter)
        self.direction_box = QComboBox()
        self.direction_box.insertItem(0, "None selected")
        self.direction_box.insertItem(1, "4-way movement")
        self.direction_box.insertItem(2, "8-way movement")
        self.direction_box.model().item(0).setEnabled(False)
        #set here

        self.search_button = QPushButton("Start Search")

        self.form_layout.addRow(self.title_label)
        self.form_layout.addRow(self.algo_label)
        self.form_layout.addRow(self.algo_box)
        self.form_layout.addRow(self.row_label)
        self.form_layout.addRow(self.row_line)
        self.form_layout.addRow(self.col_label)
        self.form_layout.addRow(self.col_line)
        self.form_layout.addRow(self.direction_label)
        self.form_layout.addRow(self.direction_box)
        self.form_layout.addRow(self.search_button)


        self.setLayout(self.form_layout)

    def on_algo_valueChanged(self, selected_algorithm: int):
        for algo in 


class GridWidget(QWidget, xy.Grid):
    def __init__(self):
        super().__init__()
        # Grid logic
        self.label = QLabel()
        self.label.setText("HELLO FROM XYGRID")

        #pyQT metadata
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.label)
        self.setLayout(self.main_layout)


    def get_node_size(self) -> tuple[int, int]:
        """ Returns dynamic height and width for a node depending on size of grid. """
        node_height = self.height//self.cols
        node_width = self.width//self.rows
        return node_height, node_width


    def create_node(self, node, pos_x, pos_y):
        """ Creates node widget drawn at specified pos_x, pos_y """
        self.grid_layout.addWidget(node, pos_x, pos_y)
        self.main_layout.setLayout(self.grid_layout)



class XYWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #pyQT metadata
        self.parent = parent
        self.main_layout = QHBoxLayout()
        #self.xy_grid = XYGrid()
        self.grid_widget = GridWidget()
        self.grid_form = GridForm()

        self.main_layout.addWidget(self.grid_form)
        self.main_layout.addWidget(self.grid_widget)
        self.setLayout(self.main_layout)
