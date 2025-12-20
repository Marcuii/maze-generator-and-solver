"""
Base pathfinder module.
Provides common functionality for all pathfinding algorithms.
"""

import math
from typing import List, Tuple, Dict, Optional


class BasePathfinder:
    """
    Abstract base class for pathfinding algorithms.
    
    Provides common functionality like neighbor detection and path reconstruction
    that all pathfinding algorithms can use.
    
    Attributes:
        maze_obj: Reference to the Maze object
        start: Starting position (row, col)
        end: Target/ending position (row, col)
        size: Size of the maze grid
        diagonal_movement: Whether diagonal movement is allowed
    """
    
    def __init__(self, maze_obj, diagonal_movement: bool = True) -> None:
        """
        Initialize the base pathfinder.
        
        Args:
            maze_obj: The Maze object containing the maze structure
            diagonal_movement: Allow diagonal moves (8 directions) if True,
                             otherwise only cardinal directions (4 directions)
        """
        self.maze_obj = maze_obj
        self.start: Tuple[int, int] = self.maze_obj.start
        self.end: Tuple[int, int] = self.maze_obj.end
        self.size: int = self.maze_obj.size
        self.diagonal_movement: bool = diagonal_movement

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get all valid neighboring cells for a given position.
        
        A neighbor is valid if:
        - It's within the maze boundaries
        - It's not a wall (maze value == 0)
        
        Args:
            row: Current row position
            col: Current column position
            
        Returns:
            List of valid neighbor positions as (row, col) tuples
        """
        neighbors: List[Tuple[int, int]] = []
        
        # Define possible movement directions
        if self.diagonal_movement:
            # 8 directions: up, down, left, right, and 4 diagonals
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                         (-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            # 4 directions: up, down, left, right only
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Check each direction
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Validate: within bounds and not a wall
            if (0 <= new_row < self.size and 0 <= new_col < self.size and
                    self.maze_obj.maze[new_row][new_col] == 0):
                neighbors.append((new_row, new_col))
                
        return neighbors

    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]], 
                          current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct the path from start to end using the came_from mapping.
        
        This method backtracks from the end position to the start position
        using the came_from dictionary that stores the parent of each cell.
        
        Args:
            came_from: Dictionary mapping each cell to its parent cell
            current: The current cell (typically the end position)
            
        Returns:
            List of positions forming the path from start to end
        """
        path: List[Tuple[int, int]] = []
        
        # Backtrack from current to start
        while current in came_from and came_from[current] is not None:
            path.append(current)
            current = came_from[current]
        
        # Add start position
        path.append(self.start)
        
        # Reverse to get path from start to end
        return path[::-1]
