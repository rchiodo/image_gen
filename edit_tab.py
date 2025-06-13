"""
Module to setup the Edit tab controls for the Image Generator App.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def setup_edit_tab(parent, app):
    """Create and pack the edit tools UI into the given parent frame."""
    tools_frame = ttk.LabelFrame(parent, text="Image Tools", padding="10")
    tools_frame.pack(fill=tk.X, pady=(10, 0))
    
    # Tool buttons
    tool_buttons = ttk.Frame(tools_frame)
    tool_buttons.pack(fill=tk.X)
    ttk.Button(tool_buttons, text="Undo", command=app.undo_edit).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(tool_buttons, text="More Pixelated", command=app.apply_more_pixelation).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(tool_buttons, text="Less Pixelated", command=app.apply_less_pixelation).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(tool_buttons, text="Remove Background", command=app.remove_background).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(tool_buttons, text="Increase Contrast", command=app.increase_contrast).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(tool_buttons, text="Increase Brightness", command=app.increase_brightness).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(tool_buttons, text="Resize Image", command=app.resize_image).pack(side=tk.LEFT)
    
    # Checkbox for automatic background removal
    ttk.Checkbutton(tools_frame, text="Auto Remove Background", variable=app.auto_remove_bg).pack(anchor=tk.W, pady=(10, 0))
