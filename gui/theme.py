"""
Theme configuration and color definitions for the maze application.
"""

from typing import Dict, Tuple


class Theme:
    """
    Application color theme and styling constants.
    
    Provides centralized theme configuration including:
    - Maze cell colors for visualization
    - UI element colors for interface components
    - Font configurations for different text elements
    - Sizing constants for layout consistency
    """
    
    # Maze cell colors (RGB hex format)
    COLORS: Dict[str, str] = {
        'start': '#00f2c3',      # Bright cyan for start position
        'end': '#ff6b9d',        # Pink for end position
        'wall': '#2d3561',       # Lighter blue-purple for walls
        'empty': '#1a1f3a',      # Darker blue for empty cells
        'exploring': '#ffd93d',  # Yellow for cells being explored
        'path': '#ff9500',       # Orange for solution path
        'outline': '#0f1419'     # Very dark outline for cell borders
    }
    
    # UI element colors (RGB hex format)
    UI_COLORS: Dict[str, str] = {
        'bg_primary': '#0f1419',     # Very dark background
        'bg_secondary': '#1a1f3a',   # Dark blue background
        'bg_tertiary': '#252b48',    # Medium blue background
        'bg_canvas': '#16192a',      # Canvas background
        'accent': '#00f2c3',         # Cyan accent color
        'accent2': '#ff6b9d',        # Pink accent color
        'text': '#e8eaed',           # Light text color
        'text_dim': '#9aa0b2'        # Dimmed text color
    }
    
    # Font configurations (family, size, weight)
    FONTS: Dict[str, Tuple[str, int, ...]] = {
        'title': ('Arial', 32, 'bold'),
        'subtitle': ('Arial', 11),
        'header': ('Arial', 20, 'bold'),
        'section': ('Arial', 13, 'bold'),
        'subsection': ('Arial', 11, 'bold'),
        'body': ('Arial', 11),
        'small': ('Arial', 10),
        'button': ('Arial', 10, 'bold')
    }
    
    # Sizing constants (pixels)
    SIDEBAR_WIDTH: int = 300
    CANVAS_PADDING: int = 12
    BUTTON_PADDING: Tuple[int, int] = (15, 10)
    SECTION_PADDING: int = 18
