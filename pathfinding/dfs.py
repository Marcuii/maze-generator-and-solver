"""
Depth-First Search (DFS) pathfinding algorithm.
Explores as far as possible along each branch before backtracking.
"""

import time
from typing import List, Tuple, Dict, Optional
from pathfinding.base_pathfinder import BasePathfinder


class DFS(BasePathfinder):
    """
    Depth-First Search algorithm implementation.
    
    DFS explores the maze by going as deep as possible along each branch
    before backtracking. It uses a stack (LIFO) to explore nodes.
    Does NOT guarantee shortest path.
    
    Time Complexity: O(V + E) where V is vertices, E is edges
    Space Complexity: O(V)
    """
    
    def __init__(self, maze_obj, diagonal_movement: bool = True) -> None:
        """
        Initialize DFS pathfinder.
        
        Args:
            maze_obj: The Maze object to solve
            diagonal_movement: Allow diagonal movement if True
        """
        super().__init__(maze_obj, diagonal_movement)

    def solve(self) -> Tuple[List[Tuple[str, Tuple[int, int]]], List[Tuple[int, int]], int, float]:
        """
        Execute the DFS algorithm to find a path from start to end.
        
        Returns:
            Tuple containing:
            - steps: List of (step_type, position) for animation
            - path: List of positions forming the solution path
            - nodes_explored: Number of nodes explored during search
            - execution_time: Time taken to execute algorithm in seconds
        """
        algorithm_start = time.perf_counter()
        
        # Initialize stack with start position (LIFO stack)
        frontier: List[Tuple[int, int]] = [self.start]
        
        # Track where we came from (for path reconstruction)
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.start: None}
        
        # Track exploration order for visualization
        exploration_order: List[Tuple[int, int]] = []

        # DFS main loop - process stack until empty or goal found
        while frontier:
            # Pop from end (LIFO - stack behavior)
            current = frontier.pop()
            exploration_order.append(current)

            # Check if we reached the goal
            if current == self.end:
                break

            # Explore all neighbors (in reverse order for consistent behavior)
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
