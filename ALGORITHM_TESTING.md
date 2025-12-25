# Algorithm Comparison Test Script

## Overview
This test script compares all 5 pathfinding algorithms in the maze solver application:
- **Breadth-First Search (BFS)**
- **Depth-First Search (DFS)**
- **Dijkstra's Algorithm**
- **A* (A-Star)**
- **Greedy Best-First Search**

## Features
✅ Tests all algorithms on the same maze for fair comparison  
✅ Measures performance metrics (execution time, path length, nodes explored)  
✅ Saves visualization images for each algorithm  
✅ Generates detailed comparison report  
✅ Identifies best performers in different categories  

## Usage

### Basic Usage
Simply run the script:
```bash
python test_algorithms.py
```

### Customization
You can customize the test parameters by editing the `main()` function in the script:

```python
def main():
    MAZE_SIZE = 25           # Size of the maze (10-30)
    DIAGONAL_MOVEMENT = True  # Allow diagonal movement (True/False)
    
    tester = AlgorithmTester(maze_size=MAZE_SIZE, diagonal_movement=DIAGONAL_MOVEMENT)
    tester.run_all_tests()
    tester.print_comparison_report()
    tester.save_text_report()
```

## Output

### Directory Structure
After running the script, an `algorithm_comparison/` directory is created with:
```
algorithm_comparison/
├── breadth-first_search_(bfs).png
├── depth-first_search_(dfs).png
├── dijkstra's_algorithm.png
├── astar_(a-star).png
├── greedy_best-first_search.png
└── comparison_report_YYYYMMDD_HHMMSS.txt
```

### Console Output
The script provides:
- Real-time progress for each algorithm
- Detailed statistics (path length, nodes explored, execution time)
- Comparison table showing all results
- Best performer awards (shortest path, most efficient, fastest)

### Image Files
Each PNG file shows:
- 🟩 **Green**: Start position
- 🟥 **Red**: End position
- 🟦 **Blue**: Explored cells during search
- 🟨 **Yellow**: Final solution path
- ⬛ **Black**: Walls

### Text Report
The text report includes:
- Test timestamp and configuration
- Comparison table
- Best performers summary

## Performance Metrics Explained

### Path Length
- Number of cells in the final solution path
- Lower is better (shorter path)
- Optimal algorithms (BFS, Dijkstra, A*) always find shortest path

### Nodes Explored
- Number of cells visited during the search
- Lower is better (more efficient)
- Indicates how "smart" the algorithm is

### Execution Time
- Time taken to find the solution (in seconds)
- Lower is better (faster)
- Varies based on algorithm complexity and maze

## Algorithm Characteristics

### BFS (Breadth-First Search)
- ✅ Guarantees shortest path
- ❌ Explores many nodes (slower)
- Best for: Unweighted graphs, finding shortest path

### DFS (Depth-First Search)
- ❌ May not find shortest path
- ✅ Very fast, explores fewer nodes
- Best for: Quick solutions when optimality isn't critical

### Dijkstra's Algorithm
- ✅ Guarantees shortest path with weighted edges
- ❌ Explores many nodes
- Best for: Weighted graphs, guaranteed optimality

### A* (A-Star)
- ✅ Guarantees shortest path
- ✅ Efficient (fewer nodes than BFS/Dijkstra)
- Best for: Balance of speed and optimality

### Greedy Best-First Search
- ❌ May not find shortest path
- ✅ Fast, uses heuristic guidance
- Best for: Quick good solutions (not necessarily optimal)

## Tips for Testing

### Small Mazes (10-15)
- Faster testing
- All algorithms perform similarly
- Good for quick comparisons

### Medium Mazes (20-30)
- Shows clear performance differences
- Recommended for typical testing
- Balances speed and complexity

### Large Mazes (30+)
- May take longer to generate/solve
- Shows dramatic differences in efficiency
- Good for stress testing

### Diagonal Movement
- **Enabled**: Allows 8-directional movement (more realistic)
- **Disabled**: Only 4-directional movement (simpler, longer paths)

## Requirements
- Python 3.x
- Pillow (PIL) for image generation: `pip install Pillow`
- All modules from the main application

## Example Results

```
🏆 BEST PERFORMERS
Shortest Path: A* (A-Star) (23 cells)
Most Efficient: A* (A-Star) (45 nodes)
Fastest: DFS (0.000055 seconds)
```

**Interpretation:**
- A* found the optimal path efficiently
- DFS was fastest but may not be optimal
- BFS/Dijkstra are thorough but explore more nodes

## Troubleshooting

### "PIL/Pillow not available"
Install Pillow: `pip install Pillow`

### "No solution found"
- Check if start and end are reachable
- Try a different maze (run again)
- Adjust WALL_PROBABILITY in config.py

### Memory issues with large mazes
- Reduce MAZE_SIZE
- Close other applications
- Increase system memory

## Advanced Usage

### Running Multiple Tests
Run the script multiple times to test on different mazes:
```bash
for i in {1..5}; do python test_algorithms.py; done
```

### Comparing Different Configurations
Test with and without diagonal movement to see the difference.

## Credits
Part of the Maze Generator and Solver Application by Marcelino Saad
