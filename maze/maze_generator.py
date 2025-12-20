"""
Maze generation module.
Handles random maze creation with guaranteed start and end points.
"""

import random
from typing import List, Tuple
from config import WALL_PROBABILITY, DEFAULT_MAZE_SIZE, MIN_MAZE_SIZE, MAX_MAZE_SIZE


class Maze:
    """
    Maze generator class that creates random mazes with walls.
    
    The maze is represented as a 2D grid where:
    - 0 represents an empty cell (walkable path)
    - 1 represents a wall (blocked cell)
    
    Attributes:
        size (int): The dimension of the square maze (size x size grid)
        maze (List[List[int]]): 2D list representing the maze structure
        start (Tuple[int, int]): Starting position (row, col)
        end (Tuple[int, int]): Ending position (row, col)
    """
    
    def __init__(self, size: int = DEFAULT_MAZE_SIZE) -> None:
        """
        Initialize the maze with the specified size.
        
        Args:
            size: The dimension of the square maze (default from config)
            
        Raises:
            ValueError: If size is not within valid range
        """
        if not (MIN_MAZE_SIZE <= size <= MAX_MAZE_SIZE):
            raise ValueError(f"Maze size must be between {MIN_MAZE_SIZE} and {MAX_MAZE_SIZE}")
        
        self.size: int = size
        self.maze: List[List[int]] = []
        self.start: Tuple[int, int] = (1, 1)
        self.end: Tuple[int, int] = (size - 2, size - 2)
        self.create_maze()

    def create_maze(self) -> None:
        """
        Generate a new random maze with walls and open paths.
        
        The maze always has:
        - Walls around all edges (border)
        - Clear start and end points
        - Random internal walls based on WALL_PROBABILITY
        - Strategic walls near start and end for challenge
        - A diagonal path to help ensure solvability
        """
        # Update end point based on current size
        self.end = (self.size - 2, self.size - 2)
        
        # Initialize maze with borders (walls on edges, empty inside)
        self.maze = [
            [1 if i == 0 or i == self.size - 1 or j == 0 or j == self.size - 1 else 0
             for j in range(self.size)] 
            for i in range(self.size)
        ]
        
        # Add random internal walls
        for i in range(2, self.size - 2):
            for j in range(2, self.size - 2):
                if random.random() < WALL_PROBABILITY:
                    self.maze[i][j] = 1
        
        # Ensure start and end are always clear
        self.maze[1][1] = self.maze[self.end[0]][self.end[1]] = 0
        
        # Add strategic walls for complexity
        self.add_strategic_walls()
        
        # Create a diagonal path to help ensure maze is solvable
        for i in range(1, min(self.size - 1, max(self.end[0], self.end[1]))):
            if i < self.size - 1:
                self.maze[i][i] = 0

    def add_strategic_walls(self) -> None:
        """
        Add strategic walls near start and end points.
        
        This method adds randomly selected walls from predefined positions
        near the start and end points to increase maze complexity while
        maintaining solvability.
        """
        # Define wall positions near start and end
        positions = [
            # Near start (top-left)
            [(1, 3), (1, 4), (2, 2), (2, 3), (3, 1), (3, 2), (4, 1)],
            # Near end (bottom-right)
            [(self.end[0] - 1, self.end[1] - 2), (self.end[0] - 2, self.end[1] - 1),
             (self.end[0] - 2, self.end[1]), (self.end[0], self.end[1] - 2),
             (self.end[0] - 3, self.end[1] - 1), (self.end[0] - 1, self.end[1] - 3)]
        ]
        
        # Randomly select and place half of the walls from each group
        for wall_group in positions:
            for row, col in random.sample(wall_group, len(wall_group) // 2):
                # Only place walls within bounds and not on start/end
                if (0 < row < self.size - 1 and 0 < col < self.size - 1 and
                        (row, col) not in [self.start, self.end]):
                    self.maze[row][col] = 1
