<h1>2D/3D Path Finder</h1>

<img src="https://raw.githubusercontent.com/henryriveraCS/path-finder/master/images/blocks.png" width="200">


Pathfinding algorithms visualized in python3 with a 2D/~~3D(soon)~~ GUI interface. 

<h2>FEATURES</h2>

1. Set starting/end points
2. Set wall points (algorithm will work around these nodes)
3. Dynamically resize the grid
4. Step-in feature to visualize how the algorithm moves each cycle


<h2>TO DO</h2>

- ~~Re-design PyQt5 widget classes to be more modular~~
- ~~Re-implement 2D Astar Algorithm~~
- ~~Re-implement 2D Djikstra Algorithm~~
- Implement 3D Astar Algorithm
- Implement 3D Djikstra Algorithm

<h2> HOW TO RUN</h2>

```bash
git clone https://github.com/henryriveraCS/path-finder
cd path-finder/
python3 -m venv ./
source bin/activate (or bin/activate.ps1 if using windows)
pip3 install -r requirements.txt
python3 path-finder/app.py
```
