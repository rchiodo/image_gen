"""
Module to setup the Generate tab controls for the Image Generator App.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


def setup_generate_tab(parent, app):
    """Create and pack the generate UI into the given parent frame."""
    chat_frame = ttk.LabelFrame(parent, text="AI Chat", padding="10")
    chat_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
    chat_frame.configure(width=300)
    
    # Chat history
    app.chat_history = scrolledtext.ScrolledText(chat_frame, width=35, height=20, wrap=tk.WORD)
    app.chat_history.pack(fill=tk.BOTH, expand=True)
    # Welcome messages
    app.chat_history.insert(tk.END, "Welcome to AI Pixelated Image Generator!\n\n")
    app.chat_history.insert(tk.END, "Enter a prompt below to generate pixel art.\n")
    app.chat_history.insert(tk.END, "Examples (just the object name):\n")
    app.chat_history.insert(tk.END, "- 'treasure chest'\n")
    app.chat_history.insert(tk.END, "- 'medieval knight'\n")
    app.chat_history.insert(tk.END, "- 'magic potion bottle'\n")
    app.chat_history.insert(tk.END, "- 'fantasy sword'\n")
    app.chat_history.insert(tk.END, "\nYou can customize the prompt template above to change\n")
    app.chat_history.insert(tk.END, "how your object is rendered. Use {prompt} as a placeholder.\n\n")
    app.chat_history.insert(tk.END, "Toggle 'Auto Remove Background' in the tools section\n")
    app.chat_history.insert(tk.END, "to control background removal.\n\n")
    
    # Prompt template section
    template_frame = ttk.LabelFrame(chat_frame, text="Prompt Template", padding="5")
    template_frame.pack(fill=tk.X, pady=(10, 0))
    template_container = ttk.Frame(template_frame)
    template_container.pack(fill=tk.X, expand=True, pady=(5, 5))
    template_scrollbar = ttk.Scrollbar(template_container, orient="vertical")
    template_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.prompt_template = tk.Text(template_container, height=4, wrap=tk.WORD, yscrollcommand=template_scrollbar.set)
    app.prompt_template.pack(side=tk.LEFT, fill=tk.X, expand=True)
    template_scrollbar.config(command=app.prompt_template.yview)
    prompt_template_text = app.load_prompt_template()
    app.prompt_template.insert(tk.END, prompt_template_text)
    
    template_actions = ttk.Frame(template_frame)
    template_actions.pack(fill=tk.X, pady=(2, 0))
    ttk.Label(template_actions, text="Use {prompt} where your input should be inserted", font=("", 8)).pack(side=tk.LEFT)
    ttk.Button(template_actions, text="Save Template", command=app.save_prompt_template).pack(side=tk.RIGHT)
    
    # Prompt input
    prompt_frame = ttk.Frame(chat_frame)
    prompt_frame.pack(fill=tk.X, pady=(10, 0))
    ttk.Label(prompt_frame, text="Prompt:").pack(anchor=tk.W)
    app.prompt_entry = tk.Text(prompt_frame, height=1, wrap=tk.WORD)
    app.prompt_entry.pack(fill=tk.X, pady=(5, 0))
    
    # Buttons
    button_frame = ttk.Frame(chat_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))
    app.generate_btn = ttk.Button(button_frame, text="Generate New", command=app.generate_image)
    app.generate_btn.pack(fill=tk.X, pady=(0, 5))
    app.modify_btn = ttk.Button(button_frame, text="Modify Current", command=app.modify_image)
    app.modify_btn.pack(fill=tk.X)
    
    # Progress bar
    app.progress = ttk.Progressbar(chat_frame, mode='indeterminate')
    app.progress.pack(fill=tk.X, pady=(10, 0))
