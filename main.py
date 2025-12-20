"""
Maze Generator and Solver Application

A modern, interactive maze generator and pathfinding visualizer built with
Python and Tkinter. This application allows users to generate random mazes
and visualize different pathfinding algorithms in real-time.

Features:
- Random maze generation with customizable sizes
- Multiple pathfinding algorithms (BFS, DFS, Dijkstra, A*)
- Real-time visualization with adjustable animation speed
- Save/load maze functionality
- Export solved mazes as PNG images
- Modern dark-themed UI

Author: Marcelino Saad
License: MIT
"""

from gui.maze_gui import EnhancedMazeGUI


def main() -> None:
    """
    Application entry point.
    
    Initializes and runs the Enhanced Maze GUI application.
    """
    app = EnhancedMazeGUI()
    app.run()


if __name__ == "__main__":
    main()
