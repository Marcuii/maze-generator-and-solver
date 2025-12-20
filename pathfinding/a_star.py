"""
A* (A-Star) pathfinding algorithm.
Combines Dijkstra's cost-based approach with heuristic guidance.
"""

import time
import heapq
import math
from typing import List, Tuple, Dict, Optional
from pathfinding.base_pathfinder import BasePathfinder
from config import DIAGONAL_COST, STRAIGHT_COST


class AStar(BasePathfinder):
    """
    A* (A-Star) pathfinding algorithm implementation.
    
    A* uses both the actual cost from start and a heuristic estimate
    to the goal, making it more efficient than Dijkstra while still
    guaranteeing the shortest path (with an admissible heuristic).
    
    Time Complexity: O((V + E) log V) in practice, better than Dijkstra
    Space Complexity: O(V)
    """
    
    def __init__(self, maze_obj, diagonal_movement: bool = True) -> None:
        """
        Initialize A* pathfinder.
        
        Args:
            maze_obj: The Maze object to solve
            diagonal_movement: Allow diagonal movement if True
        """
        super().__init__(maze_obj, diagonal_movement)

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """
        Calculate Manhattan distance heuristic between two points.
        
        Manhattan distance is admissible (never overestimates) for grid-based
        pathfinding, which guarantees A* finds the optimal path.
        
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
        Execute the A* algorithm to find the shortest path.
        
        Returns:
            Tuple containing:
            - steps: List of (step_type, position) for animation
            - path: List of positions forming the solution path
            - nodes_explored: Number of nodes explored during search
            - execution_time: Time taken to execute algorithm in seconds
        """
        algorithm_start = time.perf_counter()
        
        # Priority queue: (f_score, position) where f_score = g_score + h_score
        frontier: List[Tuple[float, Tuple[int, int]]] = [(0, self.start)]
        
        # Track where we came from
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.start: None}
        
        # Track actual cost from start (g_score)
        cost_so_far: Dict[Tuple[int, int], float] = {self.start: 0}
        
        # Track exploration order for visualization
        exploration_order: List[Tuple[int, int]] = []

        # A* main loop
        while frontier:
            # Get cell with lowest f_score (g + h)
            _, current = heapq.heappop(frontier)
            exploration_order.append(current)

            # Check if we reached the goal
            if current == self.end:
                break

            # Explore all neighbors
            for neighbor in self.get_neighbors(current[0], current[1]):
                # Calculate movement cost (g_score)
                if self.diagonal_movement:
                    # Check if diagonal move
                    is_diagonal = abs(current[0] - neighbor[0]) + abs(current[1] - neighbor[1]) == 2
                    cost = DIAGONAL_COST if is_diagonal else STRAIGHT_COST
                else:
                    cost = STRAIGHT_COST
                
                # Calculate new g_score (actual cost from start)
                new_cost = cost_so_far[current] + cost
                
                # Update if this is a better path to the neighbor
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    # f_score = g_score + h_score (heuristic)
                    priority = new_cost + self.heuristic(neighbor, self.end)
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
