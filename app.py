from PyQt5.QtCore import QSize, Qt, QRectF, QPoint
from PyQt5.QtWidgets import (
                            QApplication, QWidget, QPushButton,
                            QMainWindow, QLabel, QVBoxLayout,
                            QHBoxLayout, QGraphicsView, QFormLayout,
                            QLineEdit, QFormLayout, QComboBox,
                            QGridLayout, QGroupBox, QListWidget,
                            QMessageBox
                            )
from PyQt5.QtGui import (
                            QPainter, QBrush, QColor,
                            QFont, QIcon
                        )

# Only needed for access to command line arguments
from OSInterface import OSInterface
import sys
import time
import math
from operator import attrgetter

class Node(QWidget):
    def __init__(self, parent, point, posX, posY, height, width):
        super(Node, self).__init__(parent)
        self.parent = parent
        self.point = point
        self.cost = 1 
        self.G = 0
        self.H = 0
        self.Parent = None
        self.distance = float(math.inf)
        self.wall = False

        #QT metadata for node
        self.backgroundColor = Qt.white
        self.wallColor = QColor(87, 133, 222)
        self.startColor = QColor(31, 222, 116)
        self.pathColor = QColor(87, 133, 222)
        self.visistedColor = QColor(255, 27, 131)
        self.endColor = QColor(222, 31, 37)
        self.isWall = False
        self.isStart = False
        self.isEnd = False
        self.isVisisted = False
        self.isPath = False
        self.height = height
        self.width = width
        self.posX = posX
        self.posY = posY
        
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
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            self.SetNoneNode()
            self.SetWallNode()

        if event.button() == Qt.LeftButton:
            self.SetNoneNode()
            #check if another start exist via parent widget
            if self.parent.startNode == None:
                self.SetStartNode()
                self.parent.startNode = self
            else:
                self.parent.msgBox.exec_()

        if event.button() == Qt.RightButton:
            if self.parent.endNode == None:
                self.SetEndNode()
                self.parent.endNode = self
            else:
                self.parent.msgBox.exec_()

    def SetNoneNode(self):
        self.isWall = False
        self.isStart = False
        self.isEnd = False
        self.backgroundColor = self.backgroundColor
        self.update()

    def SetEndNode(self):
        self.isWall = False
        self.isStart = False
        self.isEnd = True
        self.backgroundColor = self.endColor
        self.update()

    def SetWallNode(self):
        self.isStart = False
        self.isEnd = False
        self.isWall = True
        self.backgroundColor = self.wallColor
        self.update()

    def SetStartNode(self):
        self.isEnd = False
        self.isWall = False
        self.isStart = True
        self.backgroundColor = self.startColor
        self.update()

    def MoveCost(self):
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
        #these values are used to prevent duplicate start/end nodes
        self.startNode = None
        self.endNode = None
        #represents size of nodes (will be updated as window size changes)
        self.gridLayout = QGridLayout()
        self.windowLayout = QVBoxLayout()
        self.HGroupBox = QGroupBox()
        self.setLayout(self.windowLayout)
        self.windowLayout.addWidget(self.HGroupBox)
        #initialize UI (Qt won't load paintEvent without minimum size being set)
        self.height = parent.osi.GetGridHeight()
        self.width = parent.osi.GetGridWidth()
        self.setMinimumSize(QSize(self.width, self.height))

        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle("Warning")
        self.msgBox.setText("Start/End node has already been selected. Please refresh to clear out your selection")

        self.initUI()
    
    def initUI(self):
        nodeHeight, nodeWidth = self.NodeSize()
        posX, posY = 0, 0
        for x in self.x_range:
            for y in self.y_range:
                node = Node(parent=self, point=(x,y), posX=posX, posY=posY, height=nodeHeight, width=nodeWidth)
                self.CreateGridLayout(node, x, y)
                self.nodeMatrix.append(node)

        self.update()
    
    #add a node widget with this function at position X,Y
    def CreateGridLayout(self, node, x, y):
        self.gridLayout.addWidget(node, x, y)
        self.HGroupBox.setLayout(self.gridLayout)

    #this function returns height,width for the node to use to draw itself
    def NodeSize(self):
        nodeHeight = self.height//self.cols
        nodeWidth = self.width//self.rows
        
        return nodeHeight, nodeWidth

    #this function is used by the main window to get all node instances from the grid and returning a list of them
    def GetNodeChildren(self):
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
        self.rowsComboBox.setCurrentIndex(9)

        self.columnsComboBox = QComboBox()
        cCount = 1
        columns = 25
        while cCount < columns:
            self.columnsComboBox.addItem(str(cCount))
            cCount += 1
        #set default here
        self.columnsComboBox.setCurrentIndex(9)

        self.speedComboBox = QComboBox()
        tCount = float(0)
        while tCount < 1:
            tmpNum = tCount + 0.10
            self.speedComboBox.addItem(str(tmpNum))
            tCount += round(tmpNum, 2)

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
        self.updateGridButton.clicked.connect(self.UpdateGridSize)

        self.aButton = QPushButton("Astar Search")
        self.dButton = QPushButton("Dijkstra Search")

        self.aButton.clicked.connect(self.aSearchClicked)
        self.dButton.clicked.connect(self.dSearchClicked)

        self.refreshButton = QPushButton("REFRESH")
        self.refreshButton.clicked.connect(self.RefreshPath)
        self.refreshButton.clicked.connect(self.RefreshGrid)

        #logic for path list
        self.listWidget = QListWidget()
        self.listLabel = QLabel()
        self.listLabel.setText("PATH TRAVERSED(end to start)")
        self.listLabel.setAlignment(Qt.AlignCenter)
    
        #layout logic
        outerLayout = QHBoxLayout()
        self.hLayout = QHBoxLayout()
        self.vLayout = QVBoxLayout()

        self.hLayout.addWidget(self.Grid)

        self.vLayout.addWidget(self.rowsLabel)
        self.vLayout.addWidget(self.rowsComboBox)
        self.vLayout.addWidget(self.columnsLabel)
        self.vLayout.addWidget(self.columnsComboBox)
        self.vLayout.addWidget(self.updateGridButton)
        self.vLayout.addWidget(self.directionLabel)
        self.vLayout.addWidget(self.directionComboBox)
        self.vLayout.addWidget(self.startPoint)
        self.vLayout.addWidget(self.endPoint)
        self.vLayout.addWidget(self.speedLabel)
        self.vLayout.addWidget(self.speedComboBox)
        self.vLayout.addWidget(self.dButton)
        self.vLayout.addWidget(self.aButton)
        self.vLayout.addWidget(self.listLabel)
        self.vLayout.addWidget(self.listWidget)
        self.vLayout.addWidget(self.refreshButton)
        self.vLayout.addStretch()

        #style vLayout with forms.css
        QPushButton.setStyleSheet(self, open(self.osi.GetStyleSheet() ).read())
            
        #add the V layer into the H layer
        outerLayout.addLayout(self.hLayout)
        outerLayout.addLayout(self.vLayout)

        container = QWidget()
        container.setLayout(outerLayout)

        self.setCentralWidget(container)

    #used to refresh the path list
    def RefreshPath(self):
        self.listWidget.clear()
    
    #used to refresh the grid
    def RefreshGrid(self):
        self.hLayout.removeWidget(self.Grid)
        self.Grid.deleteLater()
        self.Grid.update()
        self.Grid = Grid(self, self.x_range, self.y_range, self.matrix, self.nodeCount)
        self.hLayout.addWidget(self.Grid)
        self.Grid.update()

    #used to update the grid size
    def UpdateGridSize(self):
        newRows = int(self.rowsComboBox.currentText()) + 1
        newCols = int(self.columnsComboBox.currentText()) + 1
        self.x_range, self.y_range = range(newRows), range(newCols)
        #this will kill the grid instance -> we can now re-initialize it with
        #the new values
        self.Grid.deleteLater()
        self.hLayout.removeWidget(self.Grid)

        self.Grid = Grid(self, self.x_range, self.y_range, self.matrix, self.nodeCount)
        self.hLayout.addWidget(self.Grid)

    
    #run when dijkstra search is clicked
    def dSearchClicked(self, checked):
        print("Beginning Dijkstra search...")
        startNode, endNode, matrix, DIRECTION, SPEED = self.GetAlgoInfo()
        #make sure a start/end node are selected before continuing
        if startNode != None and endNode != None:
            #update the label of start node + end node
            self.startPoint.setText("START NODE: " + str(startNode.point))
            self.endPoint.setText("END NODE: " + str(endNode.point))
            self.DijkstraAlgorithm(startNode, endNode, matrix, DIRECTION, SPEED)
        else:
            print("Please select a start/end node!", startNode, endNode)
    
    #used by both algo's to determine the neighbors
    def Neighbors(self, currentNode, matrix, DIRECTION):
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
    def DijkstraAlgorithm(self, startNode, endNode, matrix, DIRECTION, SPEED):
        vSet = [] #visited nodes
        uSet = matrix #unvisted nodes

        #first iteration will be starting node with a distance of 0
        startNode.distance = 0
        currentNode = startNode
        uSet.remove(currentNode)
        while currentNode != endNode:
            neighborNodes = self.Neighbors(currentNode, matrix, DIRECTION)
            #mark every neighbor as visited
            for node in neighborNodes:
                node.isVisisted = True
                node.repaint()
                tentativeCost = currentNode.distance + node.MoveCost()
                if node in vSet or node.isWall == True:
                    continue
                else:
                    if tentativeCost < node.distance:
                        node.distance = tentativeCost
                        node.Parent = currentNode
                        for i in uSet:
                            if i.point == node.point:
                                i = node
            vSet.append(currentNode)
            lowestCostNode = min(uSet, key=attrgetter("distance"))
            currentNode = lowestCostNode
            uSet.remove(currentNode)
            
        #now that algo finished -> go through the node parents of the end node to find the path
        count = 0
        #we have to create a list (from start to end) to properly draw everything
        fixedList = []
        while currentNode.Parent:
            fixedList.append(currentNode)
            currentNode = currentNode.Parent

        for currentNode in fixedList[::-1]:
            currentNode.isVisisted = False
            currentNode.repaint()
            currentNode.isPath = True
            #call the repaint function to color in the node
            currentNode.repaint()
            #time.sleep the length the user chose
            time.sleep(SPEED)
            print("Path to final node: ", currentNode.point)
            #update the color of the node to represent the walked path
            self.listWidget.insertItem(count, str(currentNode.point))
            count += 1
    
    #this function is called by both algos in order to get the necessary data (start, end, matrix, direction)
    def GetAlgoInfo(self):
        #get the nodes in the grid
        currentGrid = self.Grid 
        #refresh grid to update data before assigning values
        currentGrid.update()
        matrix = currentGrid.GetNodeChildren()
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
    def ManhattanDistance(self, currentNode, goalNode):
        nodeX, nodeY = currentNode.point
        goalX, goalY = goalNode.point

        dx = abs(nodeX - goalX)
        dy = abs(nodeY - goalY)
        cost = currentNode.cost
        return cost * (dx+dy)

    def aSearchClicked(self, checked):
        print("Beginning A* search...")
        startNode, endNode, matrix, DIRECTION, SPEED = self.GetAlgoInfo()
        #make sure a start/end node are selected before continuing
        if startNode != None and endNode != None:
            #update the label of start node + end node
            self.startPoint.setText("START NODE: " + str(startNode.point))
            self.endPoint.setText("END NODE: " + str(endNode.point))
            #astar returns a final path
            closedSet = self.astarAlgorithm(startNode, endNode, matrix, DIRECTION, SPEED)
            count = 0
            #for node in closedSet[::-1]:
            for node in closedSet:
                #to prevent duplicate start node don't display the first node
                if node != closedSet[0]:
                    print("Path to final node: ", node.point)
                    self.listWidget.insertItem(count, str(node.point))
                    node.isVisisted = False
                    node.isPath = True
                    node.repaint()
                    count += 1
            print("FINISHED")
        else:
            print("Please select a start/end node!", startNode, endNode)
    
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
                while currentNode.Parent:
                    finalPath.append(currentNode.Parent)
                    currentNode = currentNode.Parent
                finalPath.append(currentNode)
                return finalPath[::-1]
            
            openSet.remove(currentNode)
            closedSet.append(currentNode)
            for node in self.Neighbors(currentNode, matrix, DIRECTION):
                node.isVisited = True
                node.repaint()
                #if the node is in the closet set/is a wall, continue
                if node in closedSet or node.isWall == True:
                    continue
                if node in openSet:
                    newG = currentNode.G + currentNode.MoveCost()
                    if node.G > newG:
                        node.G = newG
                        node.Parent = currentNode
                else:
                    node.G = currentNode.G + currentNode.MoveCost()
                    node.H = self.ManhattanDistance(node, endNode)
                    node.Parent = currentNode
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
