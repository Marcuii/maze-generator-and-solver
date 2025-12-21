"""
TTK style configurations for the maze application.
"""

from tkinter import ttk
from typing import Dict


class StyleManager:
    """
    Manages ttk widget styles for the application.
    
    Configures all ttk widget styles with the application theme,
    including buttons, labels, checkbuttons, scrollbars, and frames.
    """
    
    def __init__(self, colors: Dict[str, str]) -> None:
        """
        Initialize the style manager.
        
        Args:
            colors: Dictionary containing UI color definitions from Theme.UI_COLORS
        """
        self.colors = colors
        self.style = ttk.Style()
        
        # Use 'clam' theme across all platforms for consistent custom styling
        # Default Windows themes often ignore background color settings
        try:
            self.style.theme_use('clam')
        except Exception:
            # Fallback to default if clam is not available
            pass
    
    def configure_all(self) -> None:
        """Configure all widget styles for the application."""
        self._configure_buttons()
        self._configure_checkbuttons()
        self._configure_labels()
        self._configure_scrollbar()
        self._configure_frames()
    
    def _configure_buttons(self) -> None:
        """
        Configure button styles.
        
        Creates three button styles:
        - Modern.TButton: Default button with tertiary background
        - Accent.TButton: Primary action button with cyan accent
        - Secondary.TButton: Secondary action button with pink accent
        """
        # Modern button style (default)
        self.style.configure('Modern.TButton', 
                           font=('Arial', 10, 'bold'), 
                           padding=(15, 10),
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text'], 
                           borderwidth=0,
                           relief='flat')
        self.style.map('Modern.TButton', 
                      background=[('active', self.colors['accent'])],
                      foreground=[('active', self.colors['bg_primary'])])
        
        # Accent button style (primary actions)
        self.style.configure('Accent.TButton', 
                           font=('Arial', 10, 'bold'), 
                           padding=(15, 10),
                           background=self.colors['accent'],
                           foreground=self.colors['bg_primary'], 
                           borderwidth=0,
                           relief='flat')
        self.style.map('Accent.TButton', 
                      background=[('active', '#00d4aa')])
        
        # Secondary button style (secondary actions)
        self.style.configure('Secondary.TButton', 
                           font=('Arial', 10, 'bold'), 
                           padding=(15, 10),
                           background=self.colors['accent2'],
                           foreground='#fff', 
                           borderwidth=0,
                           relief='flat')
        self.style.map('Secondary.TButton', 
                      background=[('active', '#ff5280')])
    
    def _configure_checkbuttons(self) -> None:
        """Configure checkbutton styles with theme colors."""
        self.style.configure('TCheckbutton', 
                           font=('Arial', 10, 'bold'), 
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text'],
                           padding=(15, 10),
                           anchor='center')
        self.style.map('TCheckbutton',
                      background=[('active', self.colors['bg_primary']),
                                 ('!active', self.colors['bg_secondary'])],
                      foreground=[('active', self.colors['text'])])
    
    def _configure_labels(self) -> None:
        """
        Configure label styles.
        
        Creates two label styles:
        - TLabel: Default label with dimmed text
        - Header.TLabel: Bold header label with bright text
        """
        self.style.configure('TLabel', 
                           font=('Arial', 10), 
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_dim'],
                           padding=(5, 5))
        
        self.style.configure('Header.TLabel', 
                           font=('Arial', 11, 'bold'), 
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text'],
                           padding=(5, 5))
    
    def _configure_scrollbar(self) -> None:
        """Configure scrollbar styles with theme colors."""
        self.style.configure('Vertical.TScrollbar',
                           background=self.colors['bg_secondary'],
                           troughcolor=self.colors['bg_tertiary'],
                           bordercolor=self.colors['bg_tertiary'],
                           arrowcolor=self.colors['text_dim'],
                           darkcolor=self.colors['bg_secondary'],
                           lightcolor=self.colors['bg_secondary'])
        self.style.map('Vertical.TScrollbar',
                      background=[('active', self.colors['bg_secondary']),
                                 ('!active', self.colors['bg_secondary'])])
    
    def _configure_frames(self) -> None:
        """Configure frame styles with theme colors."""
        self.style.configure('Sidebar.TFrame',
                           background=self.colors['bg_tertiary'])
