"""
Custom themed dialog components for the maze application.
"""

import tkinter as tk
from typing import Dict, Any, Optional


class ThemedDialog:
    """
    Custom themed dialogs to replace standard tkinter dialogs.
    
    Provides info, warning, and error dialogs that match the
    application's dark theme, improving visual consistency.
    """
    
    @staticmethod
    def _create_dialog(parent: Any, title: str, message: str, 
                      colors: Dict[str, str], button_color: str, 
                      button_fg: str = '#fff') -> None:
        """
        Base dialog creation method used by all dialog types.
        
        Creates a centered, modal dialog with custom styling that
        matches the application theme.
        
        Args:
            parent: The parent window for the dialog
            title: Dialog window title
            message: Message text to display
            colors: Dictionary of UI theme colors
            button_color: Background color for the OK button
            button_fg: Foreground (text) color for the OK button
        """
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.configure(bg=colors['bg_secondary'])
        dialog.resizable(False, False)
        dialog.transient(parent)  # Keep on top of parent
        dialog.grab_set()  # Make modal
        
        # Center dialog on parent window
        dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 150) // 2
        dialog.geometry(f"400x150+{x}+{y}")
        
        # Message label with word wrapping
        msg_label = tk.Label(
            dialog, text=message, font=('Arial', 11), 
            fg=colors['text'], bg=colors['bg_secondary'],
            wraplength=350, justify='left', padx=20, pady=20
        )
        msg_label.pack(expand=True, fill='both')
        
        # OK button frame and button
        btn_frame = tk.Frame(dialog, bg=colors['bg_secondary'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        ok_btn = tk.Button(
            btn_frame, text="OK", font=('Arial', 10, 'bold'),
            bg=button_color, fg=button_fg,
            activebackground=button_color, activeforeground=button_fg,
            relief='flat', padx=30, pady=8, cursor='hand2',
            command=dialog.destroy
        )
        ok_btn.pack()
        
        # Wait for user to close dialog
        dialog.wait_window()
    
    @staticmethod
    def show_info(parent: Any, title: str, message: str, 
                  colors: Dict[str, str]) -> None:
        """
        Show an informational dialog with custom theming.
        
        Uses the accent color (cyan) for the OK button.
        
        Args:
            parent: The parent window for the dialog
            title: Dialog window title
            message: Information message to display
            colors: Dictionary of UI theme colors
        """
        ThemedDialog._create_dialog(
            parent, title, message, colors, 
            colors['accent'], colors['bg_primary']
        )
    
    @staticmethod
    def show_warning(parent: Any, title: str, message: str, 
                     colors: Dict[str, str]) -> None:
        """
        Show a warning dialog with custom theming.
        
        Prepends a warning emoji and uses yellow for the OK button.
        
        Args:
            parent: The parent window for the dialog
            title: Dialog window title
            message: Warning message to display
            colors: Dictionary of UI theme colors
        """
        ThemedDialog._create_dialog(
            parent, title, f"⚠️ {message}", colors, 
            '#ffd93d', '#0f1419'
        )
    
    @staticmethod
    def show_error(parent: Any, title: str, message: str, 
                   colors: Dict[str, str]) -> None:
        """
        Show an error dialog with custom theming.
        
        Prepends an error emoji and uses pink (accent2) for the OK button.
        
        Args:
            parent: The parent window for the dialog
            title: Dialog window title
            message: Error message to display
            colors: Dictionary of UI theme colors
        """
        ThemedDialog._create_dialog(
            parent, title, f"❌ {message}", colors, 
            colors['accent2'], '#fff'
        )
