import sys
import time
from typing import Optional

from PyQt5.QtWidgets import (
        QWidget, QGridLayout, QFormLayout,
        QLineEdit, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QComboBox,
        QMessageBox
        )

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QEvent, QThread
from PyQt5.QtGui import QPainter, QBrush, QFont

from tools import Colors
from algorithms import logic


algorithm_box_data = [
    {"index": 0, "name": "No algorithm selected", "active": False},
    {"index": 1, "name": "Astar Algorithm", "active": True},
    {"index": 2, "name": "Djikstra Algorithm", "active": True}
]

time_box_data = [
    {"index": 0, "name": "Instant", "active": False, "timer": 0},
    {"index": 1, "name": "1 step every 0.5 seconds", "active": True, "timer": 0.5},
    {"index": 2, "name": "1 step every 1.0 seconds", "active": True, "timer": 1.0},
    {"index": 3, "name": "1 step every 1.5 seconds", "active": True, "timer": 1.5},
    {"index": 4, "name": "1 step every 2.0 seconds", "active": True, "timer": 2.0}
]

direction_box_data = [
    {"index": 0, "name": "None selected", "active": False, "direction": 0},
    {"index": 1, "name": "4-way movement", "active": True, "direction": 4},
    {"index": 2, "name": "8-way movement", "active": True, "direction": 8},
]


class NodeWidget(QWidget, logic.Node):
    def __init__(self, parent):
        super().__init__(parent)
        #qt metadata
        self.parent = parent
        self.setContentsMargins(0, 0, 0, 0)
        self.background_color = Colors.white
        self.wall_border_color = Colors.black
        self.wall_color = Colors.blue
        self.start_color = Colors.dark_green
        self.path_color = Colors.dark_yellow
        self.end_color = Colors.dark_red
        self.visited_color = Colors.dark_cyan
        
        self.font_size = 15
        self.font_type = "Arial"
        self.font_style = QFont(self.font_type, self.font_size)
        self.point_label = QLabel()
        self.point_label.setStyleSheet("color:black; border:1px solid black;")

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.point_label)
        self.setLayout(self.main_layout)

    def update_point_label(self) -> None:
        self.point_label.setText(str(self.point))
        self.point_label.setFont(self.font_style)
        self.point_label.adjustSize()

    def update_font_size(self, size: int) -> None:
        self.font_size = size
        self.update_point_label()


    def paintEvent(self, parent) -> None:
        #self.setStyleSheet("background-color: rgb(255,255,255); border:1px solid rgb(0, 0, 0); ")
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHints(qp.Antialiasing)
        brush = QBrush(self.background_color)
        qp.setBrush(brush)
        if self.is_wall:
            brush = QBrush(self.wall_color)
            qp.setBrush(brush)
        if self.is_visited:
            brush = QBrush(self.visited_color)
            qp.setBrush(brush)
        if self.is_path:
            brush = QBrush(self.path_color)
            qp.setBrush(brush)
        if self.is_start:
            brush = QBrush(self.start_color)
            qp.setBrush(brush)
        if self.is_end:
            brush = QBrush(self.end_color)
            qp.setBrush(brush)
        qp.drawRect(0, 0, self.width(), self.height())
        qp.end()


    def mousePressEvent(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.parent.set_start_node(self)
        elif event.button() == Qt.RightButton:
            self.parent.set_end_node(self)
        self.parent.refresh_nodes()


class GridForm(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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
        self.row_line.editingFinished.connect(self.on_row_changed)

        self.col_label = QLabel()
        self.col_label.setText("Columns:")
        self.col_label.setAlignment(Qt.AlignCenter)
        self.col_line = QLineEdit()
        self.col_line.setText(str(self.rows))
        self.col_line.editingFinished.connect(self.on_col_changed)

        self.reload_button = QPushButton("Reload Grid")
        self.reload_button.clicked.connect(self.on_reload_grid)

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
        self.form_layout.addRow(self.reload_button)
        self.form_layout.addRow(self.search_button)

        self.setLayout(self.form_layout)


    def show_msg_box(self, title: str, msg: str) -> None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.exec_()


    def on_col_changed(self) -> None:
        title="Invalid Column"
        msg = "Column is not an integer"
        col_is_int = self.col_line.text().isdigit()
        if col_is_int:
            self.cols = int(self.col_line.text())
        else:
            self.cols = 5
            self.col_line.setText(str(self.cols))
            self.show_msg_box(title=title, msg=msg)


    def on_row_changed(self) -> None:
        title="Invalid Row"
        msg = "Row is not an integer"
        row_is_int = self.row_line.text().isdigit()
        if row_is_int:
            self.rows = int(self.row_line.text())
        else:
            self.rows = 5
            self.row_line.setText(str(self.rows))
            self.show_msg_box(title=title, msg=msg)


    @pyqtSlot()
    def on_reload_grid(self) -> None:
        """ Reloads entire grid with selected row/columns """
        self.parent.reload_grid()


    @pyqtSlot(int)
    def on_algo_valueChanged(self, selected_algorithm: int) -> None:
        """ Updates selected algorithm """
        self.selected_algorithm = selected_algorithm


    @pyqtSlot(int)
    def on_direction_valueChanged(self, selected_direction: int) -> None:
        """ Sets direction that algorithm will use """
        for direction in direction_box_data:
            if selected_direction == direction.get("index"):
                self.selected_direction = direction.get("direction")


    @pyqtSlot(int)
    def on_time_valueChanged(self, selected_time: int) -> None:
        """ Sets sleep timer for algorithm steps """
        for time in time_box_data:
            if selected_time == time.get("index"):
                self.selected_time = time.get("timer")

    
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
            params = {
                "rows": self.rows,
                "cols": self.cols,
                "timer": self.selected_time,
                "direction": self.selected_direction,
                "algorithm": self.selected_algorithm
            }
            self.parent.on_valid_menu(params)
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

            title = "Missing Fields"
            self.show_msg_box(title=title, msg=msg)


class GridWidget(QWidget, logic.Grid):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        #pyQT metadata
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)
        self.setStyleSheet("margin:0px; padding:0px;")

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)


    def paintEvent(self, parent):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHints(qp.Antialiasing)
        brush = QBrush(Colors.white)
        qp.setBrush(brush)

        qp.drawRect(0, 0, self.width(), self.height())
        qp.end()

    def refresh_nodes(self) -> None:
        """ Redraws every node in the grid. """
        self.all_node_widgets = (self.grid_layout.itemAt(i) for i in range(self.grid_layout.count()))
        for node_widget in self.all_node_widgets:
            node_widget.widget().update()

    def load_nodes(self) -> None:
        """ Iteratively loads nodes set in self.matrix. """
        node_list = []
        for idx, node in enumerate(self.matrix):
            col, row = node.get_x(), node.get_y()
            node_widget = NodeWidget(parent=self)
            node_widget.set_point(row, col)
            node_widget.update_point_label()
            node_list.append(node_widget)
            self.grid_layout.addWidget(node_widget, col, row)
        self.matrix = node_list


    def get_node_size(self) -> tuple[int, int]:
        """ Returns dynamic height and width for a node depending on size of grid. """
        node_height = self.height//self.cols
        node_width = self.width//self.rows
        return node_height, node_width


class Worker(QThread):
    """ Worker object to run while loop to prevent GUI from freezing. """
    gui_update = pyqtSignal()
    def __init__(self, grid_widget, *kwargs):
        super().__init__()
        self.grid_widget = grid_widget


    def run(self):
        solved = self.grid_widget.grid_widget.is_solved
        while solved is not True:
            # astar algorithm
            if self.grid_widget.algo == 1:
                self.grid_widget.grid_widget.astar_step()
                solved = self.grid_widget.grid_widget.is_solved
            # djikstra algorithm
            elif self.grid_widget.algo == 2:
                pass

            if self.grid_widget.timer is not None:
                time.sleep(self.grid_widget.timer)

            self.gui_update.emit()
            self.grid_widget.refresh_grid()

        self.grid_widget.update()
        self.grid_widget.refresh_grid()
        self.gui_update.emit()


class XYWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #pyQT metadata
        self.parent = parent
        self.main_layout = QHBoxLayout()
        self.grid_form = GridForm(self)
        self.grid_widget = GridWidget(parent=self)

        self.main_layout.addWidget(self.grid_form)
        self.main_layout.addWidget(self.grid_widget)
        self.setLayout(self.main_layout)

        # track rows/cols
        self.rows = 5
        self.cols = 5
        self.grid_widget.set_x(val=self.cols)
        self.grid_widget.set_y(val=self.rows)
        self.load_grid()


    def on_valid_menu(self, params: dict) -> None:
        """ Runs the selected algorithm with selected options. """
        self.rows = params.get("rows")
        self.cols = params.get("cols")
        self.algo = params.get("algorithm")
        self.timer = params.get("timer")
        # making thread to prevent freezing UI while looping
        self.thread = Worker(self, self.grid_widget)
        self.parent.app.processEvents()
        self.thread.start()

    def update_layout(self) -> None:
        """ Reloads entire layout. """
        self.main_layout.deleteLater()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.grid_form)
        self.main_layout.addWidget(self.grid_widget)
        self.setLayout(self.main_layout)


    def create_grid(self, rows: int, cols: int) -> None:
        """ Creates new grid node matrix. """
        self.grid_widget = GridWidget(parent=self)
        self.grid_widget.set_x(rows)
        self.grid_widget.set_y(cols)


    def load_grid(self) -> None:
        """ Loads new grid node matrix. """
        self.grid_widget.load_matrix()
        self.grid_widget.load_nodes()

    
    def refresh_grid(self) -> None:
        self.grid_widget.refresh_nodes()

    def reload_grid(self, rows: int, cols: int) -> None:
        """ Deletes old grid and places new one with updated matrix. """
        self.main_layout.removeWidget(self.grid_widget)
        self.create_grid(rows=rows, cols=cols)
        self.load_grid()
        self.main_layout.addWidget(self.grid_widget)
        self.update()
