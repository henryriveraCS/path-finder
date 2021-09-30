#this file deals with interacting with the OS by returning paths/file names/
#iterating through files/ etc
import os
import json

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
