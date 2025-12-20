"""
Breadth-First Search (BFS) pathfinding algorithm.
Guarantees shortest path in unweighted graphs.
"""

import time
from typing import List, Tuple, Dict, Optional
from pathfinding.base_pathfinder import BasePathfinder


class BFS(BasePathfinder):
    """
    Breadth-First Search algorithm implementation.
    
    BFS explores the maze level by level, guaranteeing the shortest path
    in terms of number of steps. It uses a queue (FIFO) to explore nodes.
    
    Time Complexity: O(V + E) where V is vertices, E is edges
    Space Complexity: O(V)
    """
    
    def __init__(self, maze_obj, diagonal_movement: bool = True) -> None:
        """
        Initialize BFS pathfinder.
        
        Args:
            maze_obj: The Maze object to solve
            diagonal_movement: Allow diagonal movement if True
        """
        super().__init__(maze_obj, diagonal_movement)

    def solve(self) -> Tuple[List[Tuple[str, Tuple[int, int]]], List[Tuple[int, int]], int, float]:
        """
        Execute the BFS algorithm to find a path from start to end.
        
        Returns:
            Tuple containing:
            - steps: List of (step_type, position) for animation
            - path: List of positions forming the solution path
            - nodes_explored: Number of nodes explored during search
            - execution_time: Time taken to execute algorithm in seconds
        """
        algorithm_start = time.perf_counter()
        
        # Initialize queue with start position (FIFO queue)
        frontier: List[Tuple[int, int]] = [self.start]
        
        # Track where we came from (for path reconstruction)
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.start: None}
        
        # Track exploration order for visualization
        exploration_order: List[Tuple[int, int]] = []

        # BFS main loop - process queue until empty or goal found
        while frontier:
            # Dequeue from front (FIFO)
            current = frontier.pop(0)
            exploration_order.append(current)

            # Check if we reached the goal
            if current == self.end:
                break

            # Explore all neighbors
            for neighbor in self.get_neighbors(current[0], current[1]):
                if neighbor not in came_from:
                    frontier.append(neighbor)
                    came_from[neighbor] = current
        
        # Reconstruct the path from start to end
        path = self._reconstruct_path(came_from, self.end)
        
        # Calculate execution time
        algorithm_time = time.perf_counter() - algorithm_start
        
        # Prepare animation steps: first exploration, then path
        steps: List[Tuple[str, Tuple[int, int]]] = [('explore', cell) for cell in exploration_order]
        steps.extend([('path', cell) for cell in path if cell not in [self.start, self.end]])
        
        return steps, path, len(exploration_order), algorithm_time
