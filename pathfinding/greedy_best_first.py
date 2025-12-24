"""
Greedy Best-First Search pathfinding algorithm.
Uses only heuristic guidance without considering path cost.
"""

import time
import heapq
from typing import List, Tuple, Dict, Optional
from pathfinding.base_pathfinder import BasePathfinder


class GreedyBestFirst(BasePathfinder):
    """
    Greedy Best-First Search algorithm implementation.
    
    Unlike A*, this algorithm only uses the heuristic to guide the search,
    ignoring the actual path cost. This makes it faster but it may not
    find the shortest path.
    
    Pros:
    - Faster than A* in many cases
    - Uses less memory
    - Good for finding any path quickly
    
    Cons:
    - Does NOT guarantee the shortest path
    - Can be misled by heuristic in complex mazes
    
    Time Complexity: O(V log V) in practice, faster than A*
    Space Complexity: O(V)
    """
    
    def __init__(self, maze_obj, diagonal_movement: bool = True) -> None:
        """
        Initialize Greedy Best-First Search pathfinder.
        
        Args:
            maze_obj: The Maze object to solve
            diagonal_movement: Allow diagonal movement if True
        """
        super().__init__(maze_obj, diagonal_movement)

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """
        Calculate Manhattan distance heuristic between two points.
        
        Args:
            a: First position (row, col)
            b: Second position (row, col)
            
        Returns:
            Manhattan distance between a and b
        """
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def solve(self) -> Tuple[List[Tuple[str, Tuple[int, int]]], List[Tuple[int, int]], int, float]:
        """
        Execute the Greedy Best-First Search algorithm to find a path.
        
        Note: This algorithm does NOT guarantee the shortest path!
        It greedily follows the heuristic, which can lead to suboptimal paths.
        
        Returns:
            Tuple containing:
            - steps: List of (step_type, position) for animation
            - path: List of positions forming a solution path (may not be optimal)
            - nodes_explored: Number of nodes explored during search
            - execution_time: Time taken to execute algorithm in seconds
        """
        algorithm_start = time.perf_counter()
        
        # Priority queue: (heuristic_score, position)
        # Only uses heuristic, not actual path cost
        frontier: List[Tuple[float, Tuple[int, int]]] = [(0, self.start)]
        
        # Track where we came from
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.start: None}
        
        # Track visited cells to avoid revisiting
        visited: set = {self.start}
        
        # Track exploration order for visualization
        exploration_order: List[Tuple[int, int]] = []

        # Greedy Best-First Search main loop
        while frontier:
            # Get cell with lowest heuristic score (closest to goal)
            _, current = heapq.heappop(frontier)
            exploration_order.append(current)

            # Check if we reached the goal
            if current == self.end:
                break

            # Explore all neighbors
            for neighbor in self.get_neighbors(current[0], current[1]):
                # Only visit each cell once (greedy approach)
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Priority is ONLY the heuristic (distance to goal)
                    priority = self.heuristic(neighbor, self.end)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        # Reconstruct the path
        path = self._reconstruct_path(came_from, self.end)
        
        # Calculate execution time
        algorithm_time = time.perf_counter() - algorithm_start
        
        # Prepare animation steps
        steps: List[Tuple[str, Tuple[int, int]]] = [('explore', cell) for cell in exploration_order]
        steps.extend([('path', cell) for cell in path if cell not in [self.start, self.end]])
        
        return steps, path, len(exploration_order), algorithm_time
