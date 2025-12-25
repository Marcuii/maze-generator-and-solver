"""
Algorithm Comparison Test Script

Compares all 5 pathfinding algorithms on the same maze and generates:
- Performance statistics (time, path length, nodes explored)
- Visual solutions saved as PNG images for each algorithm
- Comparison report

Author: Algorithm Tester
"""

import os
import time
from typing import List, Tuple, Dict, Any
from datetime import datetime

from maze.maze_generator import Maze
from pathfinding.bfs import BFS
from pathfinding.dfs import DFS
from pathfinding.dijkstra import Dijkstra
from pathfinding.a_star import AStar
from pathfinding.greedy_best_first import GreedyBestFirst
from config import EXPORT_CELL_SIZE

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. Images will not be saved.")
    print("Install with: pip install Pillow")


class AlgorithmTester:
    """Test and compare pathfinding algorithms"""
    
    # Color scheme for visualization (RGB tuples)
    COLORS = {
        'empty': (26, 31, 58),        # Bright cyan for start position
        'wall': (45, 53, 97),         # Pink for end position
        'start': (0, 242, 195),       # Lighter blue-purple for walls
        'end': (255, 107, 157),       # Darker blue for empty cells
        'exploring': (255, 217, 61),  # Yellow for cells being explored
        'path': (255, 149, 0),        # Orange for solution path
        'outline': (15, 20, 25)       # Very dark outline for cell borders
    }
    
    def __init__(self, maze_size: int = 17, diagonal_movement: bool = False):
        """
        Initialize the algorithm tester.
        
        Args:
            maze_size: Size of the maze to generate (default: 25)
            diagonal_movement: Allow diagonal movement in pathfinding (default: True)
        """
        self.maze_size = maze_size
        self.diagonal_movement = diagonal_movement
        self.maze_obj = None
        self.results: Dict[str, Dict[str, Any]] = {}
        
        # Create output directory for images
        self.output_dir = "algorithm_comparison"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🎯 Algorithm Comparison Test")
        print(f"{'=' * 60}")
        print(f"Maze Size: {maze_size}x{maze_size}")
        print(f"Diagonal Movement: {diagonal_movement}")
        print(f"Output Directory: {self.output_dir}/")
        print(f"{'=' * 60}\n")
    
    def generate_maze(self) -> None:
        """Generate a new maze for testing"""
        print("🔨 Generating maze...")
        self.maze_obj = Maze(self.maze_size)
        print(f"✓ Maze generated successfully")
        print(f"  Start: {self.maze_obj.start}")
        print(f"  End: {self.maze_obj.end}\n")
    
    def test_algorithm(self, name: str, algorithm_class) -> Dict[str, Any]:
        """
        Test a single algorithm and collect statistics.
        
        Args:
            name: Name of the algorithm
            algorithm_class: Class of the algorithm to test
            
        Returns:
            Dictionary containing test results
        """
        print(f"🧪 Testing {name}...")
        
        try:
            # Create algorithm instance
            algo = algorithm_class(self.maze_obj, self.diagonal_movement)
            
            # Run the algorithm
            start_time = time.perf_counter()
            steps, path, nodes_explored, algo_time = algo.solve()
            end_time = time.perf_counter()
            
            # Calculate statistics
            total_time = end_time - start_time
            path_length = len(path)
            found_solution = len(path) > 0
            
            result = {
                'name': name,
                'success': found_solution,
                'path_length': path_length,
                'nodes_explored': nodes_explored,
                'execution_time': algo_time,
                'total_time': total_time,
                'steps': steps,
                'path': path
            }
            
            # Print results
            if found_solution:
                print(f"  ✓ Solution found!")
                print(f"    Path Length: {path_length} cells")
                print(f"    Nodes Explored: {nodes_explored}")
                print(f"    Execution Time: {algo_time:.6f} seconds")
            else:
                print(f"  ✗ No solution found")
            
            return result
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return {
                'name': name,
                'success': False,
                'error': str(e)
            }
    
    def save_solution_image(self, name: str, result: Dict[str, Any]) -> None:
        """
        Save the algorithm solution as a PNG image.
        
        Args:
            name: Name of the algorithm
            result: Result dictionary containing steps and path
        """
        if not PIL_AVAILABLE:
            return
        
        if not result.get('success', False):
            print(f"  ⚠ Skipping image save (no solution found)")
            return
        
        try:
            # Image settings
            cell_size = EXPORT_CELL_SIZE
            width = self.maze_size * cell_size
            height = self.maze_size * cell_size
            
            # Create image
            img = Image.new('RGB', (width, height), self.COLORS['empty'])
            draw = ImageDraw.Draw(img)
            
            # Draw maze structure
            for i in range(self.maze_size):
                for j in range(self.maze_size):
                    x1, y1 = j * cell_size, i * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    
                    # Determine cell color
                    if (i, j) == self.maze_obj.start:
                        color = self.COLORS['start']
                    elif (i, j) == self.maze_obj.end:
                        color = self.COLORS['end']
                    elif self.maze_obj.maze[i][j] == 1:  # Wall
                        color = self.COLORS['wall']
                    else:  # Empty
                        color = self.COLORS['empty']
                    
                    draw.rectangle([x1, y1, x2, y2], fill=color, outline=self.COLORS['outline'])
            
            # Draw explored cells
            for step_type, cell in result['steps']:
                if step_type == 'explore' and cell not in [self.maze_obj.start, self.maze_obj.end]:
                    i, j = cell
                    x1, y1 = j * cell_size, i * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    draw.rectangle([x1, y1, x2, y2], fill=self.COLORS['exploring'], 
                                 outline=self.COLORS['outline'])
            
            # Draw solution path
            for step_type, cell in result['steps']:
                if step_type == 'path' and cell not in [self.maze_obj.start, self.maze_obj.end]:
                    i, j = cell
                    x1, y1 = j * cell_size, i * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    draw.rectangle([x1, y1, x2, y2], fill=self.COLORS['path'], 
                                 outline=self.COLORS['outline'])
            
            # Redraw start and end points
            si, sj = self.maze_obj.start
            draw.rectangle([sj * cell_size, si * cell_size, 
                          (sj + 1) * cell_size, (si + 1) * cell_size], 
                          fill=self.COLORS['start'], outline=self.COLORS['outline'])
            
            ei, ej = self.maze_obj.end
            draw.rectangle([ej * cell_size, ei * cell_size, 
                          (ej + 1) * cell_size, (ei + 1) * cell_size], 
                          fill=self.COLORS['end'], outline=self.COLORS['outline'])
            
            # Save image
            filename = f"{name.lower().replace(' ', '_').replace('*', 'star')}.png"
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath)
            print(f"  💾 Image saved: {filepath}")
            
        except Exception as e:
            print(f"  ✗ Error saving image: {str(e)}")
    
    def run_all_tests(self) -> None:
        """Run all algorithm tests"""
        # Define algorithms to test
        algorithms = [
            ("Breadth-First Search (BFS)", BFS),
            ("Depth-First Search (DFS)", DFS),
            ("Dijkstra's Algorithm", Dijkstra),
            ("A* (A-Star)", AStar),
            ("Greedy Best-First Search", GreedyBestFirst)
        ]
        
        # Generate maze once for all algorithms
        self.generate_maze()
        
        # Test each algorithm
        for name, algo_class in algorithms:
            result = self.test_algorithm(name, algo_class)
            self.results[name] = result
            
            # Save solution image
            if result.get('success', False):
                self.save_solution_image(name, result)
            
            print()  # Blank line between tests
    
    def print_comparison_report(self) -> None:
        """Print a detailed comparison report of all algorithms"""
        print("\n" + "=" * 80)
        print("📊 ALGORITHM COMPARISON REPORT")
        print("=" * 80)
        
        # Filter successful results
        successful = {name: res for name, res in self.results.items() if res.get('success', False)}
        
        if not successful:
            print("❌ No algorithms found a solution!")
            return
        
        # Print header
        print(f"\n{'Algorithm':<30} {'Path':<8} {'Explored':<10} {'Time (s)':<12} {'Status'}")
        print("-" * 80)
        
        # Print each result
        for name, result in self.results.items():
            if result.get('success', False):
                status = "✓ Success"
                path_len = result['path_length']
                explored = result['nodes_explored']
                exec_time = f"{result['execution_time']:.6f}"
            else:
                status = "✗ Failed"
                path_len = "-"
                explored = "-"
                exec_time = "-"
            
            print(f"{name:<30} {str(path_len):<8} {str(explored):<10} {exec_time:<12} {status}")
        
        # Find best performers
        if successful:
            print("\n" + "-" * 80)
            print("🏆 BEST PERFORMERS")
            print("-" * 80)
            
            # Shortest path
            shortest = min(successful.items(), key=lambda x: x[1]['path_length'])
            print(f"Shortest Path: {shortest[0]} ({shortest[1]['path_length']} cells)")
            
            # Fewest nodes explored (most efficient)
            most_efficient = min(successful.items(), key=lambda x: x[1]['nodes_explored'])
            print(f"Most Efficient: {most_efficient[0]} ({most_efficient[1]['nodes_explored']} nodes)")
            
            # Fastest execution
            fastest = min(successful.items(), key=lambda x: x[1]['execution_time'])
            print(f"Fastest: {fastest[0]} ({fastest[1]['execution_time']:.6f} seconds)")
        
        print("\n" + "=" * 80)
        
        if PIL_AVAILABLE:
            print(f"\n📁 Solution images saved in: {self.output_dir}/")
        
        print("\n✅ Testing complete!")
    
    def save_text_report(self) -> None:
        """Save the comparison report to a text file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.output_dir, f"comparison_report_{timestamp}.txt")
        
        try:
            with open(report_file, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("ALGORITHM COMPARISON REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Maze Size: {self.maze_size}x{self.maze_size}\n")
                f.write(f"Diagonal Movement: {self.diagonal_movement}\n")
                f.write(f"Start Position: {self.maze_obj.start}\n")
                f.write(f"End Position: {self.maze_obj.end}\n\n")
                
                f.write("-" * 80 + "\n")
                f.write(f"{'Algorithm':<30} {'Path':<8} {'Explored':<10} {'Time (s)':<12} {'Status'}\n")
                f.write("-" * 80 + "\n")
                
                for name, result in self.results.items():
                    if result.get('success', False):
                        status = "Success"
                        path_len = result['path_length']
                        explored = result['nodes_explored']
                        exec_time = f"{result['execution_time']:.6f}"
                    else:
                        status = "Failed"
                        path_len = "-"
                        explored = "-"
                        exec_time = "-"
                    
                    f.write(f"{name:<30} {str(path_len):<8} {str(explored):<10} {exec_time:<12} {status}\n")
                
                # Best performers section
                successful = {name: res for name, res in self.results.items() if res.get('success', False)}
                if successful:
                    f.write("\n" + "-" * 80 + "\n")
                    f.write("BEST PERFORMERS\n")
                    f.write("-" * 80 + "\n")
                    
                    shortest = min(successful.items(), key=lambda x: x[1]['path_length'])
                    f.write(f"Shortest Path: {shortest[0]} ({shortest[1]['path_length']} cells)\n")
                    
                    most_efficient = min(successful.items(), key=lambda x: x[1]['nodes_explored'])
                    f.write(f"Most Efficient: {most_efficient[0]} ({most_efficient[1]['nodes_explored']} nodes)\n")
                    
                    fastest = min(successful.items(), key=lambda x: x[1]['execution_time'])
                    f.write(f"Fastest: {fastest[0]} ({fastest[1]['execution_time']:.6f} seconds)\n")
                
                f.write("\n" + "=" * 80 + "\n")
            
            print(f"📄 Text report saved: {report_file}")
            
        except Exception as e:
            print(f"⚠ Warning: Could not save text report: {str(e)}")


def main():
    """Main entry point for the algorithm comparison test"""
    # You can customize these parameters
    MAZE_SIZE = 17           # Size of the maze (17x17)
    DIAGONAL_MOVEMENT = False  # Allow diagonal movement
    
    # Create tester and run
    tester = AlgorithmTester(maze_size=MAZE_SIZE, diagonal_movement=DIAGONAL_MOVEMENT)
    tester.run_all_tests()
    tester.print_comparison_report()
    tester.save_text_report()


if __name__ == "__main__":
    main()
