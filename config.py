"""
Application configuration settings.
Centralizes all constants and configuration values for easy customization.
"""

# ============================
# Maze Configuration
# ============================

# Default maze size (grid will be SIZE x SIZE)
DEFAULT_MAZE_SIZE = 15

# Minimum and maximum allowed maze sizes
MIN_MAZE_SIZE = 10
MAX_MAZE_SIZE = 30

# Probability of a cell being a wall during random generation (0.0 to 1.0)
WALL_PROBABILITY = 0.35


# ============================
# Animation Configuration
# ============================

# Default animation speed in milliseconds (lower = faster)
DEFAULT_ANIMATION_SPEED = 20

# Minimum animation speed (fastest)
MIN_ANIMATION_SPEED = 1

# Maximum animation speed (slowest)
MAX_ANIMATION_SPEED = 100


# ============================
# Canvas & Display Configuration
# ============================

# Default cell size in pixels
DEFAULT_CELL_SIZE = 20

# Minimum cell size (for large mazes)
MIN_CELL_SIZE = 15

# Maximum cell size (for small mazes)
MAX_CELL_SIZE = 25

# Divisor used to calculate cell size based on maze size
CELL_SIZE_DIVISOR = 400


# ============================
# Window Configuration
# ============================

# Application window title
WINDOW_TITLE = "🎯 Maze Explorer"

# Application window subtitle
WINDOW_SUBTITLE = "Visualize pathfinding algorithms"

# Whether to start the window maximized
START_MAXIMIZED = True


# ============================
# File Configuration
# ============================

# Default file extensions for maze files
MAZE_FILE_EXTENSION = ".txt"
IMAGE_FILE_EXTENSION = ".png"

# Image export cell size (for PNG export)
EXPORT_CELL_SIZE = 20

# File encoding for maze files
FILE_ENCODING = "utf-8"


# ============================
# Algorithm Configuration
# ============================

# Default diagonal movement setting
DEFAULT_DIAGONAL_MOVEMENT = False

# Cost for diagonal movement in A* and Dijkstra
DIAGONAL_COST = 1.414  # sqrt(2)

# Cost for straight movement
STRAIGHT_COST = 1.0


# ============================
# Logging Configuration
# ============================

# Enable/disable logging
ENABLE_LOGGING = True

# Log file name
LOG_FILE = "maze_app.log"

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "INFO"
