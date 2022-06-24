import os
import json

from PyQt5.QtCore import Qt

class Colors:
    white = Qt.white
    black = Qt.black
    red = Qt.red
    blue = Qt.blue
    green = Qt.green
    magenta = Qt.magenta
    cyan = Qt.cyan
    dark_cyan = Qt.darkCyan
    dark_yellow = Qt.darkYellow
    dark_green = Qt.darkGreen
    dark_blue = Qt.darkBlue
    dark_red = Qt.darkRed
    dark_magenta = Qt.darkMagenta


class OSInterface:
    def __init__(self):
        self.cwd = self.CurrentDirectory()
        self.configFile = "config.json"
        with open(self.configFile) as f:
            self.data = json.load(f)
            self.appTitle = self.data["AppTitle"]
            self.height = int(self.data["Height"])
            self.width = int(self.data["Width"])
            self.iconPath = self.cwd + self.data["WindowIcon"]
            self.styleSheetPath = self.cwd + self.data["StyleSheet"]
            self.gridHeight = int(self.data["GridHeight"])
            self.gridWidth = int(self.data["GridWidth"])

    def CurrentDirectory(self):
        return os.getcwd() + "/"

    def GetStyleSheet(self):
        return self.styleSheetPath

    def GetWindowsIcon(self):
        return self.iconPath

    def GetHeight(self):
        return self.height

    def GetWidth(self):
        return self.width

    def GetTitle(self):
        return self.appTitle

    def GetGridHeight(self):
        return self.gridHeight

    def GetGridWidth(self):
        return self.gridWidth
