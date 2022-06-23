import sys

from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QGridLayout, QFormLayout, QLineEdit,
        QVBoxLayout, QHBoxLayout, QPushButton,
        QLabel, QComboBox, QMessageBox

        )
from PyQt5.QtCore import QSize, Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from tools import Colors
from algorithms import grid_logic


algorithm_box_data = [
    {"index": 0, "name": "No algorithm selected", "active": False},
    {"index": 1, "name": "Astar Algorithm", "active": True},
    {"index": 2, "name": "Djikstra Algorithm", "active": True}
]

time_box_data = [
    {"index": 0, "name": "Instant", "active": False},
    {"index": 1, "name": "1 step per second", "active": True},
    {"index": 2, "name": "2 step per second", "active": True},
    {"index": 3, "name": "3 step per second", "active": True},
    {"index": 4, "name": "4 step per second", "active": True}
]

direction_box_data = [
    {"index": 0, "name": "None selected", "active": False, "direction": 0},
    {"index": 1, "name": "4-way movement", "active": True, "direction": 4},
    {"index": 2, "name": "8-way movement", "active": True, "direction": 8},
]


class NodeWidget(QWidget, grid_logic.Node):
    def __init__(self, parent, point, pos_x, pos_y, height, width):
        super(Node, self).__init__(parent, point, pos_x, pos_y, height, width)
        self.parent = parent
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
        self.selected_algorithm = None
        self.selected_direction = None
        self.selected_time = None

        
        self.title_label = QLabel()
        self.title_label.setText("2D Search Menu")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.algo_label = QLabel()
        self.algo_label.setText("Selected search algorithm")
        self.algo_label.setAlignment(Qt.AlignCenter)

        self.algo_box = QComboBox()
        for algo in algorithm_box_data:
            self.algo_box.insertItem(algo.get("index"), algo.get("name"))
            self.algo_box.model().item(algo.get("index")).setEnabled(algo.get("active"))
        self.algo_box.currentIndexChanged.connect(slot=self.on_algo_valueChanged)

        self.time_label = QLabel()
        self.time_label.setText("Algorithm Speed")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.time_box = QComboBox()
        for data in time_box_data:
            self.time_box.insertItem(data.get("index"), data.get("name"))
            self.time_box.model().item(data.get("index")).setEnabled(data.get("active"))
        self.time_box.currentIndexChanged.connect(slot=self.on_time_valueChanged)

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
        for direction in direction_box_data:
            self.direction_box.insertItem(direction.get("index"), direction.get("name"))
            self.direction_box.model().item(direction.get("index")).setEnabled(direction.get("active"))

        self.direction_box.currentIndexChanged.connect(slot=self.on_direction_valueChanged)

        self.search_button = QPushButton("Start Search")
        self.search_button.clicked.connect(self.on_search_clicked)

        self.form_layout.addRow(self.title_label)
        self.form_layout.addRow(self.algo_label)
        self.form_layout.addRow(self.algo_box)
        self.form_layout.addRow(self.direction_label)
        self.form_layout.addRow(self.direction_box)
        self.form_layout.addRow(self.time_label)
        self.form_layout.addRow(self.time_box)
        self.form_layout.addRow(self.row_label)
        self.form_layout.addRow(self.row_line)
        self.form_layout.addRow(self.col_label)
        self.form_layout.addRow(self.col_line)
        self.form_layout.addRow(self.search_button)

        self.setLayout(self.form_layout)

    @pyqtSlot(int)
    def on_algo_valueChanged(self, selected_algorithm: int) -> None:
        self.selected_algorithm = selected_algorithm


    @pyqtSlot(int)
    def on_direction_valueChanged(self, selected_direction: int) -> None:
        self.selected_direction = selected_direction


    @pyqtSlot(int)
    def on_time_valueChanged(self, selected_time: int) -> None:
        self.selected_time = selected_time

    
    @pyqtSlot()
    def on_search_clicked(self) -> None:
        """
        Validates all data from the menu and passes it to Grid if valid.
        Will display any errors if found in a QMessageBox() instance.
        """
        try:
            self.rows = int(self.row_line.text())
        except ValueError:
            self.rows = 0
        try:
            self.cols = int(self.col_line.text())
        except ValueError:
            self.cols = 0

        selected_cols_is_valid = (self.cols > 0)
        selected_rows_is_valid = (self.rows > 0)
        selected_algorithm_is_valid = (self.selected_algorithm is not None)
        selected_direction_is_valid = (self.selected_direction is not None)
        if (
            selected_algorithm_is_valid
            and selected_direction_is_valid
            and selected_rows_is_valid
            and selected_cols_is_valid
        ):
            print("set properly")
        else:
            missing_items = []
            if not selected_algorithm_is_valid:
                missing_items.append("Algorithm not selected.")
            if not selected_direction_is_valid:
                missing_items.append("Direction not chosen.")
            if not selected_rows_is_valid:
                missing_items.append("Rows must be an int greater than 0.")
            if not selected_cols_is_valid:
                missing_items.append("Columns must be an int greater than 0.")

            msg = "Make sure the following values are set correctly:\n\n"
            for item in missing_items:
                msg += f"- {item}\n"
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Missing Fields")
            msg_box.setText(msg)
            msg_box.exec_()


class GridWidget(QWidget, grid_logic.Grid):
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


    def create_nodes(self, node, pos_x, pos_y):
        """ Creates node widget and adds them dynamically """
        pass


    def on_update_algo(self, selected_algo: dict):
        """ Called when selected search algorithm is updated in GridForm. """


class XYWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #pyQT metadata
        self.parent = parent
        self.main_layout = QHBoxLayout()
        self.grid_widget = GridWidget()
        self.grid_form = GridForm()

        self.main_layout.addWidget(self.grid_form)
        self.main_layout.addWidget(self.grid_widget)
        self.setLayout(self.main_layout)
