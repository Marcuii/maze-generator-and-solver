"""
Dijkstra's pathfinding algorithm.
Finds the shortest path in weighted graphs (considers diagonal movement cost).
"""

import time
import heapq
import math
from typing import List, Tuple, Dict, Optional
from pathfinding.base_pathfinder import BasePathfinder
from config import DIAGONAL_COST, STRAIGHT_COST


class Dijkstra(BasePathfinder):
    """
    Dijkstra's shortest path algorithm implementation.
    
    Dijkstra's algorithm finds the shortest path in a weighted graph.
    It considers the cost of movement (diagonal vs straight).
    Guarantees shortest path.
    
    Time Complexity: O((V + E) log V) with binary heap
    Space Complexity: O(V)
    """
    
    def __init__(self, maze_obj, diagonal_movement: bool = True) -> None:
        """
        Initialize Dijkstra pathfinder.
        
        Args:
            maze_obj: The Maze object to solve
            diagonal_movement: Allow diagonal movement if True
        """
        super().__init__(maze_obj, diagonal_movement)

    def solve(self) -> Tuple[List[Tuple[str, Tuple[int, int]]], List[Tuple[int, int]], int, float]:
        """
        Execute Dijkstra's algorithm to find the shortest path.
        
        Returns:
            Tuple containing:
            - steps: List of (step_type, position) for animation
            - path: List of positions forming the solution path
            - nodes_explored: Number of nodes explored during search
            - execution_time: Time taken to execute algorithm in seconds
        """
        algorithm_start = time.perf_counter()
        
        # Priority queue: (cost, position)
        frontier: List[Tuple[float, Tuple[int, int]]] = [(0, self.start)]
        
        # Track where we came from
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.start: None}
        
        # Track cumulative cost to reach each cell
        cost_so_far: Dict[Tuple[int, int], float] = {self.start: 0}
        
        # Track exploration order for visualization
        exploration_order: List[Tuple[int, int]] = []

        # Dijkstra main loop
        while frontier:
            # Get cell with lowest cost
            _, current = heapq.heappop(frontier)
            exploration_order.append(current)

            # Check if we reached the goal
            if current == self.end:
                break

            # Explore all neighbors
            for neighbor in self.get_neighbors(current[0], current[1]):
                # Calculate movement cost (diagonal vs straight)
                if self.diagonal_movement:
                    # Manhattan distance to check if diagonal
                    is_diagonal = abs(current[0] - neighbor[0]) + abs(current[1] - neighbor[1]) == 2
                    cost = DIAGONAL_COST if is_diagonal else STRAIGHT_COST
                else:
                    cost = STRAIGHT_COST
                
                # Calculate new cumulative cost
                new_cost = cost_so_far[current] + cost
                
                # Update if this is a better path to the neighbor
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
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
