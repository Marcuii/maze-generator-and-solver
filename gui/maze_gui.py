"""
Refactored Maze GUI - Main application class.
Cleaner structure with separated concerns into multiple modules.
"""

import tkinter as tk
from tkinter import ttk

from maze.maze_generator import Maze
from pathfinding.bfs import BFS
from pathfinding.dfs import DFS
from pathfinding.dijkstra import Dijkstra
from pathfinding.a_star import AStar

from gui.theme import Theme
from gui.dialogs import ThemedDialog
from gui.styles import StyleManager
from gui.file_manager import MazeFileManager


class EnhancedMazeGUI:
    """Main GUI class for the maze solver application"""
    
    def __init__(self):
        """Initialize the GUI"""
        self.window = tk.Tk()
        self.window.title("🎯 Maze Explorer")
        self.window.configure(bg=Theme.UI_COLORS['bg_primary'])
        
        # Use theme colors
        self.colors = Theme.COLORS
        self.ui_colors = Theme.UI_COLORS
        
        # Initialize state variables
        self.cell_size = 20
        self.animation_speed = tk.IntVar(value=20)
        self.is_animating = False
        self.animation_steps = []
        self.current_step = 0
        self.edit_mode = tk.BooleanVar(value=False)
        self.diagonal_movement = tk.BooleanVar(value=False)
        
        # Initialize maze
        self.maze_obj = Maze()
        self.size = self.maze_obj.size
        self.start = self.maze_obj.start
        self.end = self.maze_obj.end
        
        # Configure styles
        self.style_manager = StyleManager(self.ui_colors)
        self.style_manager.configure_all()
        
        # Create UI
        self.create_widgets()
        self.draw_maze()
    
    def create_widgets(self):
        """Create the main widget layout"""
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
        # Create sidebar and main content
        sidebar = self._create_sidebar_frame()
        main_frame = self._create_main_frame()
        
        # Build components
        self._build_main_content(main_frame)
        self._build_sidebar_controls(sidebar)
    
    def _create_sidebar_frame(self):
        """Create the sidebar frame"""
        sidebar = tk.Frame(self.window, bg=self.ui_colors['bg_tertiary'], 
                          width=Theme.SIDEBAR_WIDTH)
        sidebar.grid(row=0, column=0, sticky='nsew')
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_propagate(False)
        return sidebar
    
    def _create_main_frame(self):
        """Create the main content frame"""
        main_frame = tk.Frame(self.window, bg=self.ui_colors['bg_primary'])
        main_frame.grid(row=0, column=1, sticky='nsew', padx=30, pady=30)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        return main_frame
    
    def _build_main_content(self, parent):
        """Build the main content area (header, canvas, info)"""
        self._create_header(parent)
        self._create_canvas_area(parent)
        self._create_info_section(parent)
    
    def _create_header(self, parent):
        """Create the header with title and subtitle"""
        header_frame = tk.Frame(parent, bg=self.ui_colors['bg_primary'])
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        
        tk.Label(header_frame, text="🎯 Maze Explorer", 
                font=Theme.FONTS['title'],
                fg=self.ui_colors['accent'], 
                bg=self.ui_colors['bg_primary']).pack(side='left')
        
        tk.Label(header_frame, text="Visualize pathfinding algorithms", 
                font=Theme.FONTS['subtitle'],
                fg=self.ui_colors['text_dim'], 
                bg=self.ui_colors['bg_primary']).pack(side='left', padx=(12, 0), pady=(8, 0))
    
    def _create_canvas_area(self, parent):
        """Create the maze canvas area"""
        canvas_container = tk.Frame(parent, bg=self.ui_colors['bg_canvas'], 
                                   highlightbackground=self.ui_colors['bg_tertiary'],
                                   highlightthickness=2)
        canvas_container.grid(row=1, column=0, sticky='nsew')
        
        self.canvas_frame = tk.Frame(canvas_container, bg=self.ui_colors['bg_canvas'])
        self.canvas_frame.pack(expand=True, padx=Theme.CANVAS_PADDING, pady=Theme.CANVAS_PADDING)
        self.update_canvas()
    
    def _create_info_section(self, parent):
        """Create stats and legend panels"""
        info_section = tk.Frame(parent, bg=self.ui_colors['bg_primary'])
        info_section.grid(row=2, column=0, sticky='ew', pady=(20, 0))
        info_section.grid_columnconfigure(0, weight=1)
        info_section.grid_columnconfigure(1, weight=0)
        
        self._create_stats_panel(info_section)
        self._create_legend_panel(info_section)
    
    def _create_stats_panel(self, parent):
        """Create the statistics panel"""
        stats_container = tk.Frame(parent, bg=self.ui_colors['bg_secondary'],
                                  highlightbackground=self.ui_colors['bg_tertiary'],
                                  highlightthickness=2)
        stats_container.grid(row=0, column=0, sticky='ew', padx=(0, 15))
        
        stats_inner = tk.Frame(stats_container, bg=self.ui_colors['bg_secondary'])
        stats_inner.pack(padx=20, pady=15, fill='both')
        
        tk.Label(stats_inner, text="📈 Statistics", 
                font=Theme.FONTS['section'],
                fg=self.ui_colors['text'], 
                bg=self.ui_colors['bg_secondary']).pack(anchor='w', pady=(0, 10))
        
        self.time_label = tk.Label(stats_inner, text="Ready to explore! 🚀", 
                                   font=Theme.FONTS['subsection'],
                                   fg=self.ui_colors['accent'], 
                                   bg=self.ui_colors['bg_secondary'],
                                   wraplength=400, justify='left')
        self.time_label.pack(anchor='w', pady=(0, 8))
        
        self.stats_label = tk.Label(stats_inner, text="Run an algorithm to see stats", 
                                    font=Theme.FONTS['small'],
                                    fg=self.ui_colors['text_dim'], 
                                    bg=self.ui_colors['bg_secondary'],
                                    wraplength=400, justify='left')
        self.stats_label.pack(anchor='w')
    
    def _create_legend_panel(self, parent):
        """Create the color legend panel"""
        legend_container = tk.Frame(parent, bg=self.ui_colors['bg_secondary'],
                                   highlightbackground=self.ui_colors['bg_tertiary'],
                                   highlightthickness=2)
        legend_container.grid(row=0, column=1, sticky='nsew')
        
        legend_inner = tk.Frame(legend_container, bg=self.ui_colors['bg_secondary'])
        legend_inner.pack(padx=20, pady=15)
        
        tk.Label(legend_inner, text="🎨 Legend", 
                font=Theme.FONTS['section'],
                fg=self.ui_colors['text'], 
                bg=self.ui_colors['bg_secondary']).pack(anchor='w', pady=(0, 10))
        
        legend_grid = tk.Frame(legend_inner, bg=self.ui_colors['bg_secondary'])
        legend_grid.pack()
        
        legend_items = [
            ("Start", self.colors['start']), ("End", self.colors['end']),
            ("Wall", self.colors['wall']), ("Exploring", self.colors['exploring']),
            ("Path", self.colors['path']), ("Empty", self.colors['empty'])
        ]
        
        for idx, (text, color) in enumerate(legend_items):
            row, col = idx // 3, idx % 3
            item_frame = tk.Frame(legend_grid, bg=self.ui_colors['bg_secondary'])
            item_frame.grid(row=row, column=col, sticky='w', padx=(0, 20), pady=4)
            
            color_box = tk.Canvas(item_frame, width=20, height=20, bg=color,
                                 highlightthickness=1, 
                                 highlightbackground=self.ui_colors['bg_tertiary'])
            color_box.pack(side='left', padx=(0, 8))
            
            tk.Label(item_frame, text=text, font=Theme.FONTS['small'],
                    fg=self.ui_colors['text'], 
                    bg=self.ui_colors['bg_secondary']).pack(side='left')
    
    def _build_sidebar_controls(self, parent):
        """Build all sidebar controls"""
        # Sidebar header
        sidebar_header = tk.Frame(parent, bg=self.ui_colors['bg_tertiary'])
        sidebar_header.grid(row=0, column=0, sticky='ew', pady=(25, 20), padx=20)
        
        tk.Label(sidebar_header, text="⚙️ Controls", 
                font=Theme.FONTS['header'],
                fg=self.ui_colors['text'], 
                bg=self.ui_colors['bg_tertiary']).pack(anchor='w')
        
        # Scrollable controls
        self._create_scrollable_controls(parent)
    
    def _create_scrollable_controls(self, parent):
        """Create scrollable frame with all control sections"""
        canvas = tk.Canvas(parent, bg=self.ui_colors['bg_tertiary'], 
                          highlightthickness=0, height=1)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview, 
                                 style='Vertical.TScrollbar')
        scrollable_frame = ttk.Frame(canvas, style='Sidebar.TFrame')
        
        scrollable_frame.bind("<Configure>",
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=Theme.SIDEBAR_WIDTH)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=1, column=0, sticky='nsew')
        scrollbar.grid(row=1, column=1, sticky='ns')
        parent.grid_rowconfigure(1, weight=1)
        
        # Add all control sections
        self._add_all_control_sections(scrollable_frame)
    
    def _add_all_control_sections(self, parent):
        """Add all control sections to scrollable frame"""
        row = 0
        row = self._add_size_section(parent, row)
        row = self._add_speed_section(parent, row)
        row = self._add_algorithms_section(parent, row)
        row = self._add_actions_section(parent, row)
        row = self._add_options_section(parent, row)
        row = self._add_file_section(parent, row)
    
    def _create_section(self, parent, row, title, icon):
        """Helper to create a section with header"""
        # Section header
        frame = tk.Frame(parent, bg=self.ui_colors['bg_tertiary'])
        frame.grid(row=row, column=0, sticky='ew', padx=Theme.SECTION_PADDING, pady=(18, 8))
        tk.Label(frame, text=f"{icon} {title}", 
                font=Theme.FONTS['subsection'],
                fg=self.ui_colors['text'], 
                bg=self.ui_colors['bg_tertiary'],
                padx=5, pady=5).pack(anchor='w')
        row += 1
        
        # Section content frame
        content = tk.Frame(parent, bg=self.ui_colors['bg_secondary'],
                          highlightbackground=self.ui_colors['bg_primary'],
                          highlightthickness=1)
        content.grid(row=row, column=0, padx=Theme.SECTION_PADDING, pady=(0, 12), sticky='ew')
        row += 1
        
        inner = tk.Frame(content, bg=self.ui_colors['bg_secondary'])
        inner.pack(fill='x', padx=10, pady=10)
        
        return row, inner
    
    def _add_size_section(self, parent, row):
        """Add maze size control section"""
        row, inner = self._create_section(parent, row, "Maze Size", "📐")
        
        self.size_var = tk.StringVar(value=str(self.size))
        size_spinbox = ttk.Spinbox(inner, from_=10, to=30, width=7, 
                                   textvariable=self.size_var, font=Theme.FONTS['body'])
        size_spinbox.pack(side='left', padx=(0, 8))
        
        ttk.Button(inner, text="Apply", command=self.change_size, 
                  style='Accent.TButton', width=13).pack(side='left')
        return row
    
    def _add_speed_section(self, parent, row):
        """Add animation speed control section"""
        row, inner = self._create_section(parent, row, "Animation Speed", "⚡")
        
        self.speed_label = tk.Label(inner, text=f"{self.animation_speed.get()} ms", 
                                    font=Theme.FONTS['small'],
                                    fg=self.ui_colors['accent'], 
                                    bg=self.ui_colors['bg_secondary'],
                                    padx=5, pady=3)
        self.speed_label.pack(anchor='w', pady=(0, 6))
        
        ttk.Scale(inner, from_=1, to=100, orient=tk.HORIZONTAL,
                  variable=self.animation_speed, 
                  command=self.change_speed).pack(fill='x')
        return row
    
    def _add_algorithms_section(self, parent, row):
        """Add pathfinding algorithms section"""
        row, inner = self._create_section(parent, row, "Pathfinding Algorithms", "🧠")
        
        algorithms = [
            ("📊  BFS", self.run_bfs),
            ("🌲  DFS", self.run_dfs),
            ("🎯  Dijkstra", self.run_dijkstra),
            ("⭐  A* Algorithm", self.run_a_star)
        ]
        
        for text, command in algorithms:
            ttk.Button(inner, text=text, command=command, 
                      style='Modern.TButton').pack(fill='x', pady=4)
        return row
    
    def _add_actions_section(self, parent, row):
        """Add maze actions section"""
        row, inner = self._create_section(parent, row, "Maze Actions", "🎲")
        
        ttk.Button(inner, text="🔄  New Maze", command=self.new_maze, 
                  style='Accent.TButton').pack(fill='x', pady=4)
        ttk.Button(inner, text="🧹  Clean Path", command=self.clean_maze, 
                  style='Modern.TButton').pack(fill='x', pady=4)
        ttk.Button(inner, text="⏹️  Stop", command=self.stop_animation, 
                  style='Secondary.TButton').pack(fill='x', pady=4)
        return row
    
    def _add_options_section(self, parent, row):
        """Add options section"""
        row, inner = self._create_section(parent, row, "Options", "⚙️")
        
        ttk.Checkbutton(inner, text="✏️  Edit Mode", 
                       variable=self.edit_mode).pack(fill='x', pady=4)
        ttk.Checkbutton(inner, text="↗️  Diagonal Movement", 
                       variable=self.diagonal_movement).pack(fill='x', pady=4)
        return row
    
    def _add_file_section(self, parent, row):
        """Add file operations section"""
        row, inner = self._create_section(parent, row, "Save & Load", "💾")
        
        ttk.Button(inner, text="💾  Save Maze", command=self.save_maze, 
                  style='Modern.TButton').pack(fill='x', pady=4)
        ttk.Button(inner, text="📂  Load Maze", command=self.load_maze, 
                  style='Modern.TButton').pack(fill='x', pady=4)
        ttk.Button(inner, text="🎨  Save Solved Maze", command=self.save_solved_maze, 
                  style='Accent.TButton').pack(fill='x', pady=4)
        return row
    
    # Canvas and drawing methods
    def update_canvas(self):
        """Update the canvas size"""
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.canvas_frame, 
                                width=self.size * self.cell_size,
                                height=self.size * self.cell_size, 
                                bg=self.ui_colors['bg_canvas'], 
                                bd=0, highlightthickness=0)
        self.canvas.pack(expand=True)
        self.canvas.bind("<Button-1>", self.canvas_click_handler)
    
    def draw_maze(self):
        """Draw the entire maze"""
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                if (i, j) == self.start:
                    color = self.colors['start']
                elif (i, j) == self.end:
                    color = self.colors['end']
                elif self.maze_obj.maze[i][j] == 1:
                    color = self.colors['wall']
                else:
                    color = self.colors['empty']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                            outline=self.colors['outline'], width=1)
    
    def draw_cell(self, row, col, color_key):
        """Draw a single cell"""
        x1, y1 = col * self.cell_size, row * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        color = self.colors.get(color_key, color_key)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                     outline=self.colors['outline'], width=1)
    
    # Event handlers
    def canvas_click_handler(self, event):
        """Handle canvas clicks for edit mode"""
        if self.edit_mode.get():
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            if (row, col) not in [self.start, self.end]:
                self.maze_obj.maze[row][col] = 1 - self.maze_obj.maze[row][col]
                self.draw_cell(row, col, 'wall' if self.maze_obj.maze[row][col] == 1 else 'empty')
                self.clean_maze()
    
    def change_size(self):
        """Change maze size"""
        try:
            new_size = int(self.size_var.get())
            if 10 <= new_size <= 30:
                self.size = new_size
                self.cell_size = max(15, min(25, 400 // self.size))
                self.maze_obj = Maze(self.size)
                self.start = self.maze_obj.start
                self.end = self.maze_obj.end
                self.update_canvas()
                self.draw_maze()
                self.time_label.config(text="📐 Maze resized!")
                self.stats_label.config(text=f"New size: {new_size}x{new_size}")
        except ValueError:
            ThemedDialog.show_error(self.window, "Error", 
                                   "Invalid size! Please enter a number between 10 and 30.", 
                                   self.ui_colors)
    
    def change_speed(self, speed):
        """Change animation speed"""
        self.animation_speed.set(int(float(speed)))
        self.speed_label.config(text=f"{int(float(speed))} ms")
    
    # Animation methods
    def animate_algorithm(self, steps, algorithm_name, execution_time, nodes_explored):
        """Start algorithm animation"""
        self.is_animating = True
        self.animation_steps = steps
        self.current_step = 0
        self.algorithm_name = algorithm_name
        self.execution_time = execution_time
        self.nodes_explored = nodes_explored
        self.draw_maze()
        self.animate_next_step()
    
    def animate_next_step(self):
        """Animate next step of algorithm"""
        if not self.is_animating or self.current_step >= len(self.animation_steps):
            return
        
        step_type, cell = self.animation_steps[self.current_step]
        if step_type == 'explore' and cell not in [self.start, self.end]:
            self.draw_cell(cell[0], cell[1], 'exploring')
        elif step_type == 'path':
            self.draw_cell(cell[0], cell[1], 'path')
        
        self.draw_cell(self.start[0], self.start[1], 'start')
        self.draw_cell(self.end[0], self.end[1], 'end')
        
        self.current_step += 1
        progress = (self.current_step / len(self.animation_steps)) * 100
        self.time_label.config(
            text=f"🔍 {self.algorithm_name} running...\n{self.current_step}/{len(self.animation_steps)} steps ({progress:.1f}%)")
        
        if self.current_step < len(self.animation_steps):
            self.window.after(self.animation_speed.get(), self.animate_next_step)
        else:
            self.is_animating = False
            path_length = sum(1 for step_type, _ in self.animation_steps if step_type == 'path')
            self.time_label.config(text=f"✅ {self.algorithm_name} Complete!\nTime: {self.execution_time:.4f}s")
            self.stats_label.config(text=f"📊 Path Length: {path_length + 2} cells\n🔎 Nodes Explored: {self.nodes_explored}")
    
    # Algorithm runners
    def run_algorithm(self, algorithm, name):
        """Run a pathfinding algorithm"""
        if self.is_animating:
            return
        
        self.clean_maze()
        solver = algorithm(self.maze_obj, self.diagonal_movement.get())
        steps, path, nodes_explored, algorithm_time = solver.solve()
        
        if path and len(path) > 1:
            self.animate_algorithm(steps, name, algorithm_time, nodes_explored)
        else:
            ThemedDialog.show_info(self.window, "No Path Found", 
                                  "Unable to find a path from start to end!", self.ui_colors)
            self.time_label.config(text=f"❌ {name} - No path found")
    
    def run_bfs(self):
        self.run_algorithm(BFS, "BFS")
    
    def run_dfs(self):
        self.run_algorithm(DFS, "DFS")
    
    def run_dijkstra(self):
        self.run_algorithm(Dijkstra, "Dijkstra")
    
    def run_a_star(self):
        self.run_algorithm(AStar, "A*")
    
    # Maze operations
    def stop_animation(self):
        """Stop the current animation"""
        self.is_animating = False
        self.time_label.config(text="⏹️ Animation stopped")
    
    def new_maze(self):
        """Generate a new maze"""
        if self.is_animating:
            self.stop_animation()
        self.clean_maze()
        self.maze_obj.create_maze()
        self.draw_maze()
        self.time_label.config(text="🎲 New maze generated!")
        self.stats_label.config(text="Ready to solve!")
    
    def clean_maze(self):
        """Clean the maze path"""
        if self.is_animating:
            self.stop_animation()
        
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in [self.start, self.end] and self.maze_obj.maze[i][j] != 1:
                    self.draw_cell(i, j, 'empty')
        
        self.draw_maze()
        self.time_label.config(text="🧹 Path cleaned!")
        self.stats_label.config(text="Ready to solve!")
    
    # File operations
    def save_maze(self):
        """Save maze to file"""
        MazeFileManager.save_maze(self.maze_obj, self.size)
    
    def load_maze(self):
        """Load maze from file"""
        new_maze, size, cell_size = MazeFileManager.load_maze(self.size_var)
        if new_maze is not None:
            self.size = size
            self.cell_size = cell_size
            self.maze_obj.size = size
            self.maze_obj.maze = new_maze
            self.maze_obj.start = (1, 1)
            self.maze_obj.end = (size - 2, size - 2)
            self.start = self.maze_obj.start
            self.end = self.maze_obj.end
            
            self.update_canvas()
            self.draw_maze()
            self.time_label.config(text="📂 Maze loaded successfully!")
            self.stats_label.config(text=f"Size: {size}x{size}")
    
    def save_solved_maze(self):
        """Save solved maze as image"""
        MazeFileManager.save_solved_maze(
            self.window, self.maze_obj, self.size, self.colors, 
            self.animation_steps, self.start, self.end, self.ui_colors
        )
    
    def run(self):
        """Run the main event loop"""
        # Maximize window after all widgets are initialized
        self.window.update_idletasks()
        self.window.attributes('-zoomed', True)
        self.window.mainloop()
