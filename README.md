# Maze Generator & Solver

A modern, interactive maze generator and pathfinding visualizer built with Python and Tkinter. Generate random mazes and watch different algorithms find the shortest path in real-time with smooth animations.

## Features

### Maze Generation
- **Random Maze Generation**: Creates unique mazes using randomized algorithms
- **Customizable Size**: Generate mazes from 10×10 to 30×30 cells
- **Guaranteed Solution**: Every maze has a valid path from start (green) to end (red)
- **Save/Load**: Save your favorite mazes and reload them later

### Pathfinding Algorithms
Visualize and compare four classic pathfinding algorithms:

- **Breadth-First Search (BFS)**: Guarantees shortest path, explores level by level
- **Depth-First Search (DFS)**: Memory efficient, explores deeply before backtracking
- **Dijkstra's Algorithm**: Weighted shortest path with uniform cost
- **A* (A-Star)**: Intelligent search using heuristics, optimal and efficient

### Visualization
- **Real-time Animation**: Watch algorithms explore the maze step-by-step
- **Adjustable Speed**: Control animation speed from 1ms to 100ms per step
- **Color-coded Visualization**:
  - 🟢 **Green**: Start position
  - 🔴 **Red**: End position
  - 🔵 **Blue**: Cells being explored
  - 🟡 **Yellow**: Final solution path
- **Statistics Display**: View nodes explored, path length, and execution time
- **Export Results**: Save solved mazes as high-quality PNG images

### Modern Dark UI
- Sleek dark theme with smooth gradients
- Custom-styled controls and dialogs
- Responsive layout with clear visual hierarchy
- Professional color scheme (#0f1419, #1a1f3a, #252b48)

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup
1. Clone this repository:
```bash
git clone https://github.com/Marcuii/maze-generator-and-solver.git
cd maze-generator-and-solver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Generating a Maze
1. Enter maze size (10-30) in the input box
2. Click "Generate Maze" to create a random maze
3. The green cell is the start, red cell is the end

### Solving a Maze
1. Select a pathfinding algorithm from the dropdown
2. Adjust animation speed if desired (lower = faster)
3. Click "Solve Maze" to visualize the algorithm
4. Watch as it explores cells (blue) and finds the path (yellow)
5. View statistics: nodes explored, path length, and time taken

### Saving and Loading
- **Save Maze**: Click "Save Maze" to save the current maze as a .txt file
- **Load Maze**: Click "Load Maze" to load a previously saved maze
- **Export Image**: After solving, click "Save Solved Maze" to export as PNG

### Keyboard Shortcuts
- Generate new maze: Just click "Generate Maze"
- Quick solve: Select algorithm and press "Solve Maze"

## Project Structure

```
maze-generator-and-solver/
├── main.py                 # Application entry point
├── config.py               # Configuration constants
├── requirements.txt        # Python dependencies
├── maze/
│   └── maze_generator.py   # Maze generation logic
├── pathfinding/
│   ├── base_pathfinder.py  # Base class for algorithms
│   ├── bfs.py              # Breadth-First Search
│   ├── dfs.py              # Depth-First Search
│   ├── dijkstra.py         # Dijkstra's Algorithm
│   └── a_star.py           # A* Algorithm
└── gui/
    ├── maze_gui.py         # Main GUI application
    ├── theme.py            # Dark theme colors
    ├── styles.py           # Widget styling
    ├── dialogs.py          # Custom themed dialogs
    └── file_manager.py     # Save/load functionality
```

## Algorithm Comparison

| Algorithm | Guarantees Shortest Path | Memory Usage | Performance | Best Use Case |
|-----------|-------------------------|--------------|-------------|---------------|
| **BFS** | ✅ Yes | Medium | Good | Unweighted graphs |
| **DFS** | ❌ No | Low | Fast | Maze solving |
| **Dijkstra** | ✅ Yes | Medium | Good | Weighted graphs |
| **A*** | ✅ Yes | Medium | Excellent | Goal-directed search |

## Configuration

Edit `config.py` to customize:
- Default maze size and range
- Wall generation probability
- Animation speed limits
- Color scheme
- Export image settings

## Technical Details

### Maze Generation
Uses randomized algorithm with configurable wall probability (default 35%). Ensures:
- Borders are always walls
- Start position (top-left area) is always open
- End position (bottom-right area) is always open

### Pathfinding
All algorithms support:
- **Diagonal movement** with cost √2 (≈1.414)
- **Straight movement** with cost 1.0
- **Neighbor validation** to prevent wall collisions
- **Path reconstruction** to trace the solution

### Error Handling
Comprehensive error handling for:
- Invalid maze dimensions
- Corrupted save files
- Missing dependencies (Pillow)
- File I/O errors
- Invalid user inputs

## Dependencies

- **Python 3.7+**: Core language
- **tkinter**: GUI framework (bundled with Python)
- **Pillow (PIL)**: Image export functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic pathfinding algorithm visualizations
- Built with Python's tkinter for cross-platform compatibility
- Uses Pillow library for high-quality image export

## Future Enhancements

- [ ] Additional algorithms (Greedy Best-First, Bidirectional Search)
- [ ] Custom start/end point selection
- [ ] Maze editing capabilities
- [ ] Multiple maze generation algorithms
- [ ] Performance benchmarking mode
- [ ] 3D maze visualization

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/Marcuii/maze-generator-and-solver/issues) page
2. Create a new issue with detailed description
3. Include error messages and screenshots if applicable

---

Made with ❤️ using Python and Tkinter
