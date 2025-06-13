"""
Module to setup the Edit tab controls for the Image Generator App.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from PIL import Image, ImageTk

# Unified icon loading: use file if exists, otherwise generate placeholder
ICON_DIR = os.path.join(os.path.dirname(__file__), 'icons')
os.makedirs(ICON_DIR, exist_ok=True)

# Prepare raw PIL images for icons; actual PhotoImages created in setup_edit_tab
ICON_SPECS = [
    ('undo','undo.png','#e74c3c'),
    ('more','more_pixelated.png','#3498db'),
    ('less','less_pixelated.png','#2ecc71'),
    ('remove_bg','remove_bg.png','#e67e22'),
    ('contrast','contrast.png','#9b59b6'),
    ('brightness','brightness.png','#f1c40f'),
    ('resize','resize.png','#95a5a6'),
]
raw_icons = {}
for key, fname, color in ICON_SPECS:
    p = os.path.join(ICON_DIR, fname)
    if os.path.exists(p):
        img = Image.open(p)
    else:
        img = Image.new('RGBA', (16,16), color)
    raw_icons[key] = img.resize((16,16))

def setup_edit_tab(parent, app):
    """Create and pack the edit tools UI into the given parent frame."""
    tools_frame = ttk.LabelFrame(parent, text="Image Tools", padding="10")
    tools_frame.pack(fill=tk.X, pady=(10, 0))
    
    # Create PhotoImage instances bound to this parent to avoid root-timing issues
    photo_icons = {}
    for key, pil_img in raw_icons.items():
        photo_icons[key] = ImageTk.PhotoImage(pil_img, master=parent)

    # Vertical tool buttons with icons
    for key, text, cmd in [
        ('undo', 'Undo', app.undo_edit),
        ('more', 'More Pixelated', app.apply_more_pixelation),
        ('less', 'Less Pixelated', app.apply_less_pixelation),
        ('remove_bg', 'Remove Background', app.remove_background),
        ('contrast', 'Increase Contrast', app.increase_contrast),
        ('brightness', 'Increase Brightness', app.increase_brightness),
        ('resize', 'Resize Image', app.resize_image),
    ]:
        btn = ttk.Button(tools_frame, text=text, command=cmd, image=photo_icons[key], compound='left')
        btn.pack(fill=tk.X, pady=2)
        btn.image = photo_icons[key]
    
    # Checkbox for automatic background removal
    ttk.Checkbutton(tools_frame, text="Auto Remove Background", variable=app.auto_remove_bg).pack(anchor=tk.W, pady=(10, 0))
