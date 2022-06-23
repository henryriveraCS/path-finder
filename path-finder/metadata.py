import importlib

class Modes:
    empty_grid_class = getattr(importlib.import_module("widgets.empty_widget"), "EmptyWidget")
    xy_grid_class = getattr(importlib.import_module("widgets.xy_grid"), "XYWindow")
    modes = [
        {"active": False, "index": 0, "name": "None Selected", "widget": empty_grid_class},
        {"active": True, "index": 1, "name": "2D Pathfinder", "widget": xy_grid_class},
        {"active": True, "index": 2, "name": "3D Pathfinder"}
    ]
