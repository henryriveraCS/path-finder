import math

class Node:
    def __init__(self, point: (int, int)):
        self.point = point
        self.parent = None
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


    def MoveCost(self):
        return self.cost

class Grid:
    def __init__(self):
        self.matrix = []
        self.direction = 4 #set to 8 to allow for diagnoal movement
        #used by algorithms to perform a step
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


    
    def load(self) -> None:
        self.matrix = []
        for x in self.x_range:
            for y in self.y_range:
                self.matrix.append(Node((x,y)))


    def set_x(self, x: int) -> None:
        self.x_range = range(x)
        self.rows = len(self.x_range)


    def set_y(self, y: int) -> None:
        self.y_range = range(y)
        self.cols = len(self.y_range)


    def set_wall_node(self, wall_node: Node) -> None:
        for node in self.matrix:
            if node == wall_node:
                wall_node.is_wall = True

    
    def set_end_node(self, end_node: Node) -> None: 
        for node in self.matrix:
            if node == end_node:
                self.end_node = end_node
                self.end_node.is_end = True


    def set_start_node(self, start_node: Node) -> None:
        for node in self.matrix:
            if node == start_node:
                self.start_node = start_node
                self.start_node.is_start = True
                self.open_set = [self.start_node]


    def astar_step(self) -> None:
        """
            Call this function in a loop in order to iteratively take a step through the Astar
            algorithm.
            E.G:
            self.current_node = None
            self.start_node = (0,0)
            self.end_node = (0,3)
            matrix = [(0,0), (0,1), (0,2), (0,3), etc]
            while start_node != end_node:
                current_node = AstarStep(start_node, end_node, matrix)
        """
        #self.open_set.append(start_node)
        self.current_node = min(self.open_set, key=lambda node: node.G + node.H)
        self.current_node.is_visited = True
        if self.current_node == self.end_node:
            while self.current_node.parent:
                self.final_path.append(self.current_node.parent)
                self.current_node.is_path = True
                self.current_node = self.current_node.parent
            self.final_path.append(self.current_node)
            #reverse list so it starts from start_node.point
            self.final_path = self.final_path[::-1]
            #remove duplicate start_node and append final node
            self.final_path.pop(0)
            self.final_path.append(self.end_node)
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
                newG = self.current_node.G + self.current_node.MoveCost()
                if node.G > newG:
                    node.G = newG
                    node.parent = self.current_node
            else:
                node.G = self.current_node.G + self.current_node.MoveCost()
                node.H = self.manhattan_distance(node, self.end_node)
                node.parent = self.current_node
                self.open_set.append(node)
