"""
File operations for saving and loading mazes.
Handles maze persistence and image export with comprehensive error handling.
"""

from tkinter import filedialog
from typing import List, Tuple, Dict, Optional, Any
from PIL import Image, ImageDraw
from gui.dialogs import ThemedDialog
from config import (
    MAZE_FILE_EXTENSION, IMAGE_FILE_EXTENSION, EXPORT_CELL_SIZE,
    FILE_ENCODING, MIN_MAZE_SIZE, MAX_MAZE_SIZE
)


class MazeFileManager:
    """
    Handles all file I/O operations for mazes.
    
    This class provides static methods for:
    - Saving mazes to text files with metadata
    - Loading mazes from text files with validation
    - Exporting solved mazes as PNG images
    """
    
    @staticmethod
    def save_maze(maze_obj: Any, size: int) -> Optional[str]:
        """
        Save the current maze to a text file with size metadata.
        
        File format:
            SIZE:15
            111111111111111
            100000000000001
            ...
        
        Args:
            maze_obj: The maze object containing the maze data
            size: The size of the maze grid
            
        Returns:
            Path where the file was saved, or None if cancelled/failed
            
        Raises:
            IOError: If file writing fails
        """
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=MAZE_FILE_EXTENSION,
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Maze"
            )
            if not file_path:
                return None
            
            # Write maze to file with UTF-8 encoding
            with open(file_path, "w", encoding=FILE_ENCODING) as f:
                # Write size metadata on first line
                f.write(f"SIZE:{size}\n")
                
                # Write maze grid data
                for row in maze_obj.maze:
                    f.write("".join(map(str, row)) + "\n")
            
            return file_path
            
        except IOError as e:
            # File write error - could be permissions or disk issues
            raise IOError(f"Failed to save maze file: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error saving maze: {str(e)}")
    
    @staticmethod
    def load_maze(size_var: Any) -> Tuple[Optional[List[List[int]]], Optional[int], Optional[int]]:
        """
        Load a maze from a text file with validation.
        
        Supports both new format (with SIZE: header) and legacy format.
        Validates maze dimensions and cell values.
        
        Args:
            size_var: Tkinter variable to update with the loaded maze size
            
        Returns:
            Tuple of (maze_data, size, cell_size) or (None, None, None) if cancelled/failed
            
        Raises:
            ValueError: If maze file is invalid or corrupted
            IOError: If file reading fails
        """
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Load Maze"
            )
            if not file_path:
                return None, None, None
            
            # Read file with UTF-8 encoding
            with open(file_path, "r", encoding=FILE_ENCODING) as f:
                lines = f.readlines()
            
            # Validate file is not empty
            if not lines:
                raise ValueError("Maze file is empty")
            
            
            try:
                size = int(lines[0].split(":")[1].strip())
            except (IndexError, ValueError):
                raise ValueError("Invalid SIZE metadata in maze file")
            
            # Validate size is within allowed range
            if not (MIN_MAZE_SIZE <= size <= MAX_MAZE_SIZE):
                raise ValueError(
                    f"Maze size {size} is out of valid range "
                    f"({MIN_MAZE_SIZE}-{MAX_MAZE_SIZE})"
                )
            
            # Parse maze grid (skip first line with SIZE)
            maze_lines = lines[1:]
            
            # Convert text lines to 2D integer array with validation
            new_maze: List[List[int]] = []
            for line_num, line in enumerate(maze_lines, start=1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Validate line length matches expected size
                if len(line) != size:
                    raise ValueError(
                        f"Line {line_num} has {len(line)} characters, "
                        f"expected {size}"
                    )
                
                # Convert characters to integers with validation
                try:
                    row = [int(c) for c in line]
                except ValueError:
                    raise ValueError(
                        f"Line {line_num} contains non-numeric characters"
                    )
                
                # Validate cell values are 0 or 1
                if any(cell not in (0, 1) for cell in row):
                    raise ValueError(
                        f"Line {line_num} contains invalid cell values "
                        f"(must be 0 or 1)"
                    )
                
                new_maze.append(row)
            
            # Validate we got the expected number of rows
            if len(new_maze) != size:
                raise ValueError(
                    f"Maze has {len(new_maze)} rows, expected {size}"
                )
            
            # Calculate appropriate cell size for display
            cell_size = max(15, min(25, 400 // size))
            
            # Update the size input box
            size_var.set(str(size))
            
            return new_maze, size, cell_size
            
        except (IOError, OSError) as e:
            raise IOError(f"Failed to read maze file: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Invalid maze file: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error loading maze: {str(e)}")
    
    @staticmethod
    def save_solved_maze(window: Any, maze_obj: Any, size: int, colors: Dict[str, Tuple[int, int, int]], 
                        animation_steps: List[Tuple[str, Tuple[int, int]]], 
                        start: Tuple[int, int], end: Tuple[int, int], 
                        ui_colors: Dict[str, str]) -> Optional[str]:
        """
        Export the solved maze visualization to a PNG image.
        
        Creates a high-resolution image showing:
        - The maze structure (walls and paths)
        - Explored cells during pathfinding
        - The final solution path
        - Start and end points
        
        Args:
            window: The parent window for dialogs
            maze_obj: The maze object containing maze structure
            size: The size of the maze grid (NxN)
            colors: Dictionary mapping cell types to RGB color tuples
            animation_steps: List of (step_type, cell) tuples from pathfinding
            start: (row, col) coordinates of start position
            end: (row, col) coordinates of end position
            ui_colors: Dictionary of UI theme colors for dialogs
            
        Returns:
            Path where the file was saved, or None if cancelled/failed
            
        Raises:
            ValueError: If animation_steps is empty (no solution to save)
            IOError: If image saving fails
        """
        # Validate that a solution exists
        if not animation_steps:
            ThemedDialog.show_warning(
                window, "No Solution", 
                "Please solve the maze first before saving!", 
                ui_colors
            )
            return None
        
        try:
            # Request save location from user
            file_path = filedialog.asksaveasfilename(
                defaultextension=IMAGE_FILE_EXTENSION,
                filetypes=[
                    ("PNG files", "*.png"), 
                    ("All files", "*.*")
                ],
                title="Export Solved Maze"
            )
            if not file_path:
                return None  # User cancelled
            
            # Calculate image dimensions
            cell_size = EXPORT_CELL_SIZE
            width = size * cell_size
            height = size * cell_size
            
            # Validate dimensions are reasonable
            max_dimension = 10000  # Prevent excessive memory usage
            if width > max_dimension or height > max_dimension:
                raise ValueError(
                    f"Image dimensions ({width}x{height}) exceed "
                    f"maximum allowed ({max_dimension}x{max_dimension})"
                )
            
            # Create image and drawing context
            try:
                img = Image.new('RGB', (width, height), colors['empty'])
                draw = ImageDraw.Draw(img)
            except Exception as e:
                raise IOError(f"Failed to create image: {str(e)}")
            
            # Draw the base maze structure
            for i in range(size):
                for j in range(size):
                    x1, y1 = j * cell_size, i * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    
                    # Determine cell color based on position and maze structure
                    if (i, j) == start:
                        color = colors['start']
                    elif (i, j) == end:
                        color = colors['end']
                    elif maze_obj.maze[i][j] == 1:  # Wall
                        color = colors['wall']
                    else:  # Empty path
                        color = colors['empty']
                    
                    # Draw cell with outline
                    draw.rectangle(
                        [x1, y1, x2, y2], 
                        fill=color, 
                        outline=colors['outline']
                    )
            
            # Draw explored cells first (cells visited during pathfinding)
            for step_type, cell in animation_steps:
                if step_type == 'explore' and cell not in [start, end]:
                    # Validate coordinates
                    i, j = cell
                    if not (0 <= i < size and 0 <= j < size):
                        continue  # Skip invalid coordinates
                    
                    x1, y1 = j * cell_size, i * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    draw.rectangle(
                        [x1, y1, x2, y2], 
                        fill=colors['exploring'], 
                        outline=colors['outline']
                    )
            
            # Draw the solution path on top (final shortest path)
            for step_type, cell in animation_steps:
                if step_type == 'path' and cell not in [start, end]:
                    # Validate coordinates
                    i, j = cell
                    if not (0 <= i < size and 0 <= j < size):
                        continue  # Skip invalid coordinates
                    
                    x1, y1 = j * cell_size, i * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size
                    draw.rectangle(
                        [x1, y1, x2, y2], 
                        fill=colors['path'], 
                        outline=colors['outline']
                    )
            
            # Redraw start and end points on top to ensure visibility
            si, sj = start
            draw.rectangle(
                [sj * cell_size, si * cell_size, 
                 (sj + 1) * cell_size, (si + 1) * cell_size], 
                fill=colors['start'], 
                outline=colors['outline']
            )
            
            ei, ej = end
            draw.rectangle(
                [ej * cell_size, ei * cell_size, 
                 (ej + 1) * cell_size, (ei + 1) * cell_size], 
                fill=colors['end'], 
                outline=colors['outline']
            )
            
            # Save image to file
            try:
                img.save(file_path)
            except Exception as e:
                raise IOError(f"Failed to save image to {file_path}: {str(e)}")
            
            # Show success dialog
            ThemedDialog.show_info(
                window, "Success", 
                f"Solved maze saved to {file_path}", 
                ui_colors
            )
            return file_path
            
        except ImportError:
            # PIL/Pillow library not installed
            ThemedDialog.show_error(
                window, "Missing Dependency", 
                "Pillow library is required to save images.\n"
                "Install it with: pip install Pillow", 
                ui_colors
            )
            return None
        except ValueError as e:
            ThemedDialog.show_error(
                window, "Validation Error", 
                f"Cannot export maze:\n{str(e)}", 
                ui_colors
            )
            return None
        except IOError as e:
            ThemedDialog.show_error(
                window, "File Error", 
                f"Failed to save image:\n{str(e)}", 
                ui_colors
            )
            return None
        except Exception as e:
            ThemedDialog.show_error(
                window, "Error", 
                f"Unexpected error:\n{str(e)}", 
                ui_colors
            )
            return None

