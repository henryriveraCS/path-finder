import math

class Node:
    """ Base logic for Node """
    def __init__(self):
        self.point = (0, 0)
        self.node_parent = None
        self.cost = 1
        self.is_wall = False
        self.G = 0
        self.H = 0
        self.distance = float(math.inf)
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_visited = False
        self.is_path = False

    def set_point(self, x: int, y: int) -> None:
        self.point = (x,y)


    def get_x(self) -> int:
        return self.point[0]

    
    def get_y(self) -> int:
        return self.point[1]


    def move_cost(self) -> int:
        return self.cost


    def clear(self) -> None:
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_visited = False
        self.is_path = False


class Grid:
    """ Base class for Grid logic """
    def __init__(self):
        self.matrix = []
        self.direction = 4 #set to 8 to allow for diagnoal movement
        self.start_node = None
        self.current_node = None
        self.end_node = None
        self.open_set = []
        self.closed_set = []
        self.final_path = []
        self.is_solved = False


    def neighbors(self, current_node: Node) -> list:
        """
        Determine neighbors of current_node 
        self.direction = 4 will allow for movements to be Up, Left, Down, Right
        self.direction = 8 will allow extended movement such as Up-Right, Left-Down, etc
        """
        x,y = current_node.point
        if self.direction == 4:
            neighbor_list = [(x-1,y), (x+1, y), (x, y-1), (x, y+1)]
        else:
            neighbor_list = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1), (x-1,y), (x+1, y), (x, y-1), (x, y+1)]

        node_list = []
        for neighbor in neighbor_list:
            for node in self.matrix:
                if neighbor == node.point:
                    node_list.append(node)

        return node_list


    def manhattan_distance(self, current_node: Node, end_node: Node) -> int:
        """ Determines manhattan distance between this
        node and the end node."""
        current_node_x, current_node_y = current_node.point
        end_node_x, end_node_y = end_node.point
        dx = abs(current_node_x - end_node_x)
        dy = abs(current_node_x - end_node_y)
        cost = current_node.cost
        return cost * (dx+dy)

    
    def load_matrix(self) -> None:
        self.matrix = []
        for x in self.x_range:
            for y in self.y_range:
                node = Node()
                node.set_point(x, y)
                self.matrix.append(node)


    def set_x(self, val: int) -> None:
        self.x_range = range(val+1)
        self.rows = len(self.x_range)


    def set_y(self, val: int) -> None:
        self.y_range = range(val+1)
        self.cols = len(self.y_range)

    def set_direction(self, direction: int) -> None:
        if direction == 4:
            self.direction = 4
        elif direction == 8:
            self.direction = 8
        else:
            self.direction = 4

    def set_wall_node(self, wall_node: Node) -> None:
        for node in self.matrix:
            if node == wall_node:
                end_node.clear()
                wall_node.is_wall = True

    
    def set_end_node(self, end_node: Node) -> None: 
        if self.end_node is not None:
            self.end_node.clear()
        for node in self.matrix:
            if node.point == end_node.point:
                node.clear()
                self.end_node = end_node
                end_node.clear()
                self.end_node.is_end = True


    def set_start_node(self, start_node: Node) -> None:
        if self.start_node is not None:
            self.start_node.clear()
        for node in self.matrix:
            if node.point == start_node.point:
                node.clear()
                self.start_node = start_node
                self.start_node.clear()
                self.start_node.is_start = True
                self.open_set = [self.start_node]


    def set_visited_node(self, visited_node: Node) -> None:
        if visited_node in self.matrix:
            visited_node.clear()
            visited_node.is_visited = True


    def set_path_node(self, path_node: Node) -> None:
        if path_node in self.matrix:
            path_node.clear()
            path_node.is_path = True


    def astar_step(self) -> None:
        """ Take a step using the astar algorithm. Last step is appended to open_set. """
        #self.open_set.append(start_node)
        self.current_node = min(self.open_set, key=lambda node: node.G + node.H)
        self.current_node.is_visited = True
        if self.current_node.point == self.end_node.point:
            while self.current_node.node_parent:
                self.final_path.append(self.current_node.node_parent)
                self.current_node.is_path = True
                self.current_node = self.current_node.node_parent
            self.final_path.append(self.current_node)
            #reverse list so it starts from start_node.point
            self.final_path = self.final_path[::-1]
            #remove duplicate start_node and append final node
            self.final_path.pop(0)
            self.final_path.append(self.end_node)
            for node in self.final_path:
                node.is_path = True
            self.is_solved = True
            return

        self.open_set.remove(self.current_node)
        self.closed_set.append(self.current_node)
        for node in self.neighbors(self.current_node):
            node.is_visited = True
            #node.repaint()
            #if the node is in the closet set/is a wall, continue
            if node in self.closed_set or node.is_wall is True:
                continue
            if node in self.open_set:
                newG = self.current_node.G + self.current_node.move_cost()
                if node.G > newG:
                    node.G = newG
                    node.node_parent = self.current_node
            else:
                node.G = self.current_node.G + self.current_node.move_cost()
                node.H = self.manhattan_distance(node, self.end_node)
                node.node_parent = self.current_node
                self.open_set.append(node)
