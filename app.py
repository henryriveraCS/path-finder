from PyQt5.QtCore import QSize, Qt, QRectF, QPoint
from PyQt5.QtWidgets import (
                            QApplication, QWidget, QPushButton,
                            QMainWindow, QLabel, QVBoxLayout,
                            QAction, QMenu, QHBoxLayout,
                            QGraphicsView, QFormLayout, QLineEdit,
                            QFormLayout, QCheckBox, QComboBox,
                            QGridLayout, QGroupBox, QListWidget
                            )
from PyQt5.QtGui import (
                            QPainter, QBrush, QColor, QFont, QMouseEvent, QCursor,
                            QIcon
                        )

#from gui_dijkstra import dijkstraNode as dNode
# Only needed for access to command line arguments
from OSInterface import OSInterface
import sys
import time
import math
from operator import attrgetter

class dijkstraNode(QWidget):
    def __init__(self, parent, point, posX, posY, height, width):
        super(dijkstraNode, self).__init__(parent)
        self.point = point
        self.cost = 1 
        self.G = 0
        self.H = 0
        self.parent = None
        self.distance = float(math.inf)
        #node parent is used to prevent weird bugs with managing windows since it also uses "parent" as a parameter
        self.nodeParent = None
        self.wall = False

        #QT metadata for node
        #this is used by Grid to determine WHERE to place the node object
        #use the size of parent window to determine how big to make the nodes
        #use parent size to determine how to draw these nodes
        #self.setMinimumSize(QSize(parent.height, parent.width))
        #self.setMaximumSize(QSize(parent.height+1, parent.width+1))
        self.backgroundColor = Qt.white
        self.wallColor = QColor(87, 133, 222)
        self.startColor = QColor(31, 222, 116)
        self.pathColor = QColor(241, 204, 102)
        self.visistedColor = QColor(255, 0, 102)
        self.endColor = QColor(222, 31, 37)
        self.isWall = False
        self.isStart = False
        self.isEnd = False
        self.isVisisted = False
        self.isPath = False
        self.nodeStatus = QLabel()
        self.height = height
        self.width = width
        self.posX = posX
        self.posY = posY
        self.nodeStatus.setText("Not Set")
        
        #initalize UI features
        self.initUI()
    
    #this function is called by GRID in order to get the new positonX + positionY of this current node instance
    #E.G: first node will tell Grid where to start the second node, second node tells Grid where to draw third node...
    def paintEvent(self, parent):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHints(qp.Antialiasing)
        #draw the walls around the node
        #setting background settings based off self.filled status:
        if self.isWall:
            brush = QBrush(self.wallColor)  
            qp.setBrush(brush)
        elif self.isStart:
            brush = QBrush(self.startColor)
            qp.setBrush(brush)
        elif self.isEnd:
            brush = QBrush(self.endColor)
            qp.setBrush(brush)
        elif self.isVisisted:
            brush = QBrush(self.visistedColor)
            qp.setBrush(brush)
        elif self.isPath:
            brush = QBrush(self.pathColor)
            qp.setBrush(brush)
        else:
            brush = QBrush(self.backgroundColor)
            qp.setBrush(brush)

        qp.drawRect(0, 0, self.width, self.height)
        qp.drawText(QPoint(5, 15), str(self.point))
        qp.end()
    
    #making the node widget clickable
    def mousePressEvent(self, event):
        #left click assigns a value to a node as a wall
        if event.button() == Qt.MidButton:
            #check if node was already filled, if it was -> un-fill it
            if self.isWall == True:
                self.isWall = False
                self.update()
            else:   
                #update the wall values
                self.setWallNode()

        #right click assigns the node as a start node
        if event.button() == Qt.LeftButton:
            if self.isWall == True:
                self.isWall = False
                self.isEnd = False
                self.isStart = True
                self.update()
            else:
                self.setStartNode()

        #middle click assigns the node as an end node
        if event.button() == Qt.RightButton:
            if self.isWall == True:
                self.isWall = False
                self.isStart = False
                self.isEnd = True
                self.update()
            else:
                self.setEndNode()

    def initUI(self):
        pass
        #print("dijkstra node loaded: ", self.point)
    
    def setEndNode(self):
        print("END NODE: ", self.point)
        self.isWall = False
        self.isStart = False
        self.isEnd = True
        self.backgroundColor = self.endColor
        self.update()

    def setWallNode(self):
        print("WALL NODE: ", self.point)
        self.isStart = False
        self.isEnd = False
        self.isWall = True
        self.backgroundColor = self.wallColor
        self.update()

    #this function is used when you select a starting node(left mouse click)
    def setStartNode(self):
        print("START NODE: ", self.point)
        self.isEnd = False
        self.isWall = False
        self.isStart = True
        self.backgroundColor = self.startColor
        self.update()

    def move_cost(self):
        return self.cost

class Grid(QWidget):
    def __init__(self, parent, x_range, y_range, matrix, nodeCount):
        super(Grid, self).__init__(parent)
        self.nodeCount = nodeCount
        self.x_range = x_range
        self.y_range = y_range
        self.rows = len(x_range)
        self.cols = len(y_range)
        self.matrix = matrix
        self.nodeMatrix = []
        #this is used for drawing
        #represents size of nodes (will be updated as window size changes)
        self.gridLayout = QGridLayout()
        self.windowLayout = QVBoxLayout()
        self.HGroupBox = QGroupBox("grid")
        self.setLayout(self.windowLayout)
        self.windowLayout.addWidget(self.HGroupBox)
        #initialize UI (Qt won't load paintEvent without minimum size being set)
        self.height = 800
        self.width = 800
        self.setMinimumSize(QSize(self.width, self.height))

        self.initUI()
    
    def initUI(self):
        #get the nodeSize that each node needs to be before calling dNode
        nodeHeight, nodeWidth = self.nodeSize()
        posX, posY = 0, 0
        for x in self.x_range:
            for y in self.y_range:
                dNode = dijkstraNode(parent=self, point=(x,y), posX=posX, posY=posY, height=nodeHeight, width=nodeWidth)
                self.createGridLayout(dNode, x, y)
                #use the nodes own values to draw each instance next to next    
                self.nodeMatrix.append(dNode)

        self.update()
    
    #add a node widget with this function at position X,Y
    def createGridLayout(self, dNode, x, y):
        self.gridLayout.addWidget(dNode, x, y)

        self.HGroupBox.setLayout(self.gridLayout)

    #this function returns height,width for the node to use to draw itself
    def nodeSize(self):
        nodeHeight = self.height//self.cols
        nodeWidth = self.width//self.rows
        
        return nodeHeight, nodeWidth

    #this function is used by the main window to get all node instances from the grid and returning a list of them
    def getNodeChildren(self):
        nodeList = []
        for x in self.x_range:
            for y in self.y_range:
                node = self.gridLayout.itemAtPosition(x,y).widget()
                nodeList.append(node)

        return nodeList

        for node in nodeList:
            print(node.point)
        return nodeList

class MainWindow(QMainWindow):
    def __init__(self, osi):
        super().__init__()

        self.osi = osi

        self.setWindowTitle(self.osi.GetTitle())
        self.setMinimumSize(QSize(self.osi.GetHeight(), self.osi.GetWidth()))

        #data for grid:
        self.x_range = range(11)
        self.y_range = range(11)
        self.nodeCount = 0
        self.matrix = []
        for x in self.x_range:
            for y in self.y_range:
                self.nodeCount += 1
                self.matrix.append((x,y))
                
        self.Grid = Grid(self, self.x_range, self.y_range, self.matrix, self.nodeCount)

        #label logic
        #aLabel = QLabel("Astar search")
        #dLabel = QLabel("Dijkstra search")
        self.nodeLabel = QLabel()
        #self.gridLabel.setAlignment(Qt.AlignCenter)
        self.nodeLabel.setText("Node Info:")
        self.nodeLabel.setAlignment(Qt.AlignCenter)

        self.rowsLabel = QLabel()
        self.rowsLabel.setText("ROWS:")
        self.rowsLabel.setAlignment(Qt.AlignCenter)
        
        self.columnsLabel = QLabel()
        self.columnsLabel.setText("COLUMNS:")
        self.columnsLabel.setAlignment(Qt.AlignCenter)

        self.startPoint = QLabel()
        self.startPoint.setText("START POINT:")
        self.startPoint.setAlignment(Qt.AlignCenter)

        self.endPoint = QLabel()
        self.endPoint.setText("END POINT:")
        self.endPoint.setAlignment(Qt.AlignCenter)
        
        self.directionLabel = QLabel()
        self.directionLabel.setText("ALLOWED DIRECTION:")
        self.directionLabel.setAlignment(Qt.AlignCenter)

        self.nodePosition = QLabel()
        self.nodePosition.setText("No node selected")
        self.nodePosition.setAlignment(Qt.AlignCenter)

        self.speedLabel = QLabel()
        self.speedLabel.setText("SPEED (default is 0.1 second per node)")
        self.speedLabel.setAlignment(Qt.AlignCenter)

        #comboBox logic
        self.rowsComboBox = QComboBox()
        rCount = 1
        rows = 25
        while rCount < rows:
            self.rowsComboBox.addItem(str(rCount)) 
            rCount += 1
        
        #set default here
        self.rowsComboBox.setCurrentIndex(4)

        self.columnsComboBox = QComboBox()
        cCount = 1
        columns = 25
        while cCount < columns:
            self.columnsComboBox.addItem(str(cCount))
            cCount += 1
        #set default
        self.columnsComboBox.setCurrentIndex(4)

        self.speedComboBox = QComboBox()
        tCount = 0
        while tCount < 1:
            self.speedComboBox.addItem(str(tCount))
            tCount += 0.1

        #form logic (node info such as position, cost, distance, etc)
        nodeFormLayout = QFormLayout()
        nodeFormLayout.addRow("cost: ", QLineEdit())
        nodeFormLayout.addRow("distance: ", QLineEdit())
        
        #add the directional combo box for 4/8 directional movement
        self.directionComboBox = QComboBox()
        self.directionComboBox.addItem(str(4))
        self.directionComboBox.addItem(str(8))

        #button logic
        self.updateGridButton = QPushButton("Update Grid")
        self.updateGridButton.clicked.connect(self.updateGridSize)

        self.aButton = QPushButton("Astar Search")
        self.dButton = QPushButton("Dijkstra Search")

        self.aButton.clicked.connect(self.aSearchClicked)
        self.dButton.clicked.connect(self.dSearchClicked)

        self.refreshGridButton = QPushButton("REFRESH GRID")
        self.refreshGridButton.clicked.connect(self.refreshGrid)

        self.refreshPathButton = QPushButton("REFRESH PATH LIST")
        self.refreshPathButton.clicked.connect(self.refreshPath)

        #logic for path list
        self.listWidget = QListWidget()
        self.listLabel = QLabel()
        self.listLabel.setText("PATH TRAVERSED(end to start)")
        self.listLabel.setAlignment(Qt.AlignCenter)
    
        #layout logic
        outerLayout = QHBoxLayout()
        self.hLayout = QHBoxLayout()
        self.vLayout = QVBoxLayout()
        #draw grid and add it to first H layer
        self.hLayout.addWidget(self.Grid)
        self.hLayout.addStretch()
        #draw forms/buttons and add it to V layer
        self.vLayout.addWidget(self.rowsLabel)
        self.vLayout.addWidget(self.rowsComboBox)
        self.vLayout.addWidget(self.columnsLabel)
        self.vLayout.addWidget(self.columnsComboBox)
        self.vLayout.addWidget(self.updateGridButton)
        self.vLayout.addWidget(self.refreshGridButton)
        #vLayout.addWidget(self.nodeLabel)
        #vLayout.addWidget(self.nodePosition)
        #vLayout.addLayout(nodeFormLayout)
        self.vLayout.addWidget(self.directionLabel)
        self.vLayout.addWidget(self.directionComboBox)
        self.vLayout.addWidget(self.startPoint)
        self.vLayout.addWidget(self.endPoint)
        self.vLayout.addWidget(self.speedLabel)
        self.vLayout.addWidget(self.speedComboBox)
        self.vLayout.addWidget(self.dButton)
        self.vLayout.addWidget(self.aButton)
        self.vLayout.addWidget(self.listLabel)
        self.vLayout.addWidget(self.refreshPathButton)
        self.vLayout.addWidget(self.listWidget)
        self.vLayout.addStretch()
        #style vLayout with forms.css
        #QPushButton.setStyleSheet(self, open(self.osi.GetStyleSheet() ).read())
            
        #add the V layer into the H layer
        outerLayout.addLayout(self.hLayout)
        outerLayout.addLayout(self.vLayout)

        container = QWidget()
        container.setLayout(outerLayout)

        #draw the grid
        self.setCentralWidget(container)

    #used to refresh the path list
    def refreshPath(self):
        self.vLayout.removeWidget(self.listWidget)
        self.listWidget = QListWidget()
        self.vLayout.addWidget(self.listWidget)
    
    #used to refresh the grid
    def refreshGrid(self):
        self.hLayout.removeWidget(self.Grid)
        self.Grid = Grid(self, self.x_range, self.y_range, self.matrix, self.nodeCount)
        self.hLayout.addWidget(self.Grid)

    #used to update the grid size
    def updateGridSize(self):
        #convert str to int
        newRows = int(self.rowsComboBox.currentText())
        newCols = int(self.columnsComboBox.currentText())
        print("NEW ROWS: ", newRows, "NEW COLS: ", newCols)
        self.x_range, self.y_range = range(newRows), range(newCols)
        #re-intialize grid with new x_range + new y_range for new rows/cols
        self.hLayout.removeWidget(self.Grid)
        self.Grid = Grid(self, self.x_range, self.y_range, self.matrix, self.nodeCount)
        #update the grid so it redraws itself
        self.hLayout.addWidget(self.Grid)

    
    #run when dijkstra search is clicked
    def dSearchClicked(self, checked):
        print("Beginning Dijkstra search...", checked)
        startNode, endNode, matrix, DIRECTION, SPEED = self.getAlgoInfo()
        #make sure a start/end node are selected before continuing
        if startNode != None and endNode != None:
            #update the label of start node + end node
            self.startPoint.setText("START NODE: " + str(startNode.point))
            self.endPoint.setText("END NODE: " + str(endNode.point))
            self.dijkstraAlgorithm(startNode, endNode, matrix, DIRECTION, SPEED)
        else:
            print("Please select a start/end node!", startNode, endNode)
    
    #used by both algo's to determine the neighbors
    def neighbors(self, currentNode, matrix, DIRECTION):
        x,y = currentNode.point
        #make sure it's an int
        DIRECTION = int(DIRECTION)

        if DIRECTION == 4:
            neighborList = [(x-1,y), (x+1, y), (x, y-1), (x, y+1)]
        else:
            neighborList = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1), (x-1,y), (x+1, y), (x, y-1), (x, y+1)]

        nodeList = []
        for neighbor in neighborList:
            for node in matrix:
                if neighbor == node.point:
                    nodeList.append(node)
            
        return nodeList
    
    #dijkstra algorithm for GUI
    def dijkstraAlgorithm(self, startNode, endNode, matrix, DIRECTION, SPEED):
        vSet = [] #visited nodes
        uSet = matrix #unvisted nodes

        #first iteration will be starting node with a distance of 0
        startNode.distance = 0
        currentNode = startNode
        uSet.remove(currentNode)
        while currentNode != endNode:
            neighborNodes = self.neighbors(currentNode, matrix, DIRECTION)
            #mark every neighbor as visited
            for node in neighborNodes:
                node.isVisisted = True
                #time.sleep(0.2)
                node.repaint()
                tentativeCost = currentNode.distance + node.move_cost()
                if node in vSet or node.isWall == True:
                    continue
                else:
                    if tentativeCost < node.distance:
                        node.distance = tentativeCost
                        node.parent = currentNode
                        for i in uSet:
                            if i.point == node.point:
                                i = node
            vSet.append(currentNode)
            lowestCostNode = min(uSet, key=attrgetter("distance"))
            currentNode = lowestCostNode
            #print("LOWEST COST NODE: ", currentNode.point)
            uSet.remove(currentNode)
            
        #now that algo finished -> go through the node parents of the end node to find the path
        count = 0
        #we have to create a list (from start to end) to properly draw everything
        fixedList = []
        while currentNode.parent:
            fixedList.append(currentNode)
            currentNode = currentNode.parent

        for currentNode in fixedList[::-1]:
            currentNode.isVisisted = False
            currentNode.repaint()
            currentNode.isPath = True
            #call the repaint function to color in the node
            currentNode.repaint()
            #time.sleep the length the user chose
            time.sleep(SPEED)
            print("path to final node: ", currentNode, currentNode.point)
            #update the color of the node to represent the walked path
            self.listWidget.insertItem(count, str(currentNode.point))
            #currentNode = currentNode.parent
            count += 1
    
    #this function is called by both algos in order to get the necessary data (start, end, matrix, direction)
    def getAlgoInfo(self):
        #get the nodes in the grid
        currentGrid = self.Grid 
        #refresh grid to update data before assigning values
        currentGrid.update()
        matrix = currentGrid.getNodeChildren()
        startNode, endNode = None, None
        wallNodes = []
        #iterate through the nodeList in order to find the start node, end node and wall nodes
        for node in matrix:
            if node.isStart == True:
                startNode = node
            if node.isEnd == True:
                endNode = node
            if node.isWall == True:
                wallNodes.append(node)

        DIRECTION = int(self.directionComboBox.currentText())
        SPEED = float(self.speedComboBox.currentText())

        return startNode, endNode, matrix, DIRECTION, SPEED
        

    #used by astar algo to determine manhattan distance to end node
    def manhattanDistance(self, currentNode, goalNode):
        nodeX, nodeY = currentNode.point
        goalX, goalY = goalNode.point

        dx = abs(nodeX - goalX)
        dy = abs(nodeY - goalY)
        cost = currentNode.cost
        return cost * (dx+dy)

    #run when astar button is clicked
    def aSearchClicked(self, checked):
        print("Beginning A* search...", checked)
        startNode, endNode, matrix, DIRECTION, SPEED = self.getAlgoInfo()
        #make sure a start/end node are selected before continuing
        if startNode != None and endNode != None:
            #update the label of start node + end node
            self.startPoint.setText("START NODE: " + str(startNode.point))
            self.endPoint.setText("END NODE: " + str(endNode.point))
            #astar returns a final path
            closedSet = self.astarAlgorithm(startNode, endNode, matrix, DIRECTION, SPEED)
            count = 0
            for node in closedSet[::-1]:
                self.listWidget.insertItem(count, str(node.point))
                node.isVisisted = False
                node.isPath = True
                node.repaint()
                count += 1
        else:
            print("Please select a start/end node!", startNode, endNode)
    
    #astar algorithm for GUI
    def astarAlgorithm(self, startNode, endNode, matrix, DIRECTION, SPEED):
        openSet = [startNode]
        closedSet = []
        while openSet:
            currentNode = min(openSet, key=lambda f: f.G + f.H)
            currentNode.isPath = True
            currentNode.isVisisted = True
            currentNode.repaint()
            time.sleep(SPEED)
            if currentNode == endNode:
                finalPath = []
                while currentNode.parent:
                    finalPath.append(currentNode.parent)
                    currentNode = currentNode.parent
                finalPath.append(currentNode)
                print("FINISHED")
                return finalPath[::-1]
            
            openSet.remove(currentNode)
            closedSet.append(currentNode)
            for node in self.neighbors(currentNode, matrix, DIRECTION):
                node.isVisited = True
                node.repaint()
                #node.isPath = True
                #if the node is in the closet set/is a wall, continue
                if node in closedSet or node.isWall == True:
                    continue
                if node in openSet:
                    newG = currentNode.G + currentNode.move_cost()
                    if node.G > newG:
                        node.G = newG
                        node.parent = currentNode
                else:
                    node.G = currentNode.G + currentNode.move_cost()
                    node.H = self.manhattanDistance(node, endNode)
                    node.parent = currentNode
                    openSet.append(node)

#app starts here
try:
    app = QApplication(sys.argv)
    #create OS Interface instance and pass it along to the main window
    osi = OSInterface()
    app.setWindowIcon(QIcon(osi.GetWindowsIcon() ))
    window = MainWindow(osi)
    window.show()

    app.exec_()
except Exception as e:
    print("Application crashed with message:\n", e)
    app.exit()
