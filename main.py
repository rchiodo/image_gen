"""
Main GUI application for AI Image Generator
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
from PIL import Image, ImageTk
import threading
import os
from datetime import datetime
import win32clipboard
import win32con
from io import BytesIO
import json

from image_generator import ImageGenerator
from image_processor import ImageProcessor

class ImageGeneratorApp:    
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pixelated Image Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Initialize components
        self.image_generator = None
        self.current_image = None
        self.current_photo = None
        self.edit_history = []  # stack for undo
        
        # User preferences
        self.auto_remove_bg = tk.BooleanVar(value=True)
        self.template_file = "prompt_template.txt"
        
        # Create output directory
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Default prompt template text
        self.default_template_text = (
            "Isometric {prompt} for cutout, with no shadows, 8-bit style, pixelated, isometric view, "
            "not on any sort of platform, but floating on a white background"
        )
        
        self.setup_ui()
        self.initialize_generator()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout: canvas on left, controls on right in tabs
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Canvas section on left
        canvas_container = ttk.Frame(main_container)
        canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.create_canvas_section(canvas_container)
        # Tabs on right
        tab_container = ttk.Frame(main_container)
        tab_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.notebook = ttk.Notebook(tab_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        # Generate tab: chat and prompt
        gen_tab = ttk.Frame(self.notebook)
        self.notebook.add(gen_tab, text="Generate")
        self.create_chat_section(gen_tab)
        # Edit tab: image editing tools
        edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(edit_tab, text="Edit")
        self.create_tools_section(edit_tab)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_canvas_section(self, parent):
        """Create the main canvas section"""
        canvas_frame = ttk.LabelFrame(parent, text="Generated Image", padding="10")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Canvas for displaying image
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # Redraw background on canvas resize
        self.canvas.bind('<Configure>', lambda event: self.create_checkered_background())
        
        # Create checkered background pattern
        self.create_checkered_background()
        
        # Scrollbars for canvas
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Canvas controls
        canvas_controls = ttk.Frame(canvas_frame)
        canvas_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(canvas_controls, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(canvas_controls, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(canvas_controls, text="Clear Canvas", command=self.clear_canvas).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(canvas_controls, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side=tk.LEFT)
    
    def create_checkered_background(self):
        """Create a checkered background pattern on the canvas"""
        # Clear any existing background
        self.canvas.delete("background")
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # If canvas isn't initialized yet, use default size
        if width <= 1 or height <= 1:
            width, height = 600, 600
        
        # Checkered pattern settings
        square_size = 20
        color1 = "#f0f0f0"  # Light gray
        color2 = "#e0e0e0"  # Slightly darker gray
        
        # Draw checkered pattern
        for row in range(0, height // square_size + 1):
            for col in range(0, width // square_size + 1):
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                
                # Alternate colors
                color = color1 if (row + col) % 2 == 0 else color2
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=color,
                    tags="background"
                )
    
    def create_chat_section(self, parent):
        """Create the chat/prompt section"""
        chat_frame = ttk.LabelFrame(parent, text="AI Chat", padding="10")
        chat_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        chat_frame.configure(width=300)
        
        # Chat history        
        self.chat_history = scrolledtext.ScrolledText(chat_frame, width=35, height=20, wrap=tk.WORD)
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        self.chat_history.insert(tk.END, "Welcome to AI Pixelated Image Generator!\n\n")
        self.chat_history.insert(tk.END, "Enter a prompt below to generate pixel art.\n")
        self.chat_history.insert(tk.END, "Examples (just the object name):\n")
        self.chat_history.insert(tk.END, "- 'treasure chest'\n")
        self.chat_history.insert(tk.END, "- 'medieval knight'\n")
        self.chat_history.insert(tk.END, "- 'magic potion bottle'\n")
        self.chat_history.insert(tk.END, "- 'fantasy sword'\n")
        self.chat_history.insert(tk.END, "\nYou can customize the prompt template above to change\n")
        self.chat_history.insert(tk.END, "how your object is rendered. Use {prompt} as a placeholder.\n\n")
        self.chat_history.insert(tk.END, "Toggle 'Auto Remove Background' in the tools section\n")
        self.chat_history.insert(tk.END, "to control background removal.\n\n")
          # Prompt template section
        template_frame = ttk.LabelFrame(chat_frame, text="Prompt Template", padding="5")
        template_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create a frame to contain text and scrollbar
        template_container = ttk.Frame(template_frame)
        template_container.pack(fill=tk.X, expand=True, pady=(5, 5))
        
        # Add scrollbar to template
        template_scrollbar = ttk.Scrollbar(template_container, orient="vertical")
        template_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Make template text area twice as big and scrollable
        self.prompt_template = tk.Text(template_container, height=4, wrap=tk.WORD, 
                                     yscrollcommand=template_scrollbar.set)
        self.prompt_template.pack(side=tk.LEFT, fill=tk.X, expand=True)
        template_scrollbar.config(command=self.prompt_template.yview)
          # Load template from file or use default
        prompt_template_text = self.load_prompt_template()
        self.prompt_template.insert(tk.END, prompt_template_text)
        
        # Label and save button in a frame
        template_actions = ttk.Frame(template_frame)
        template_actions.pack(fill=tk.X, pady=(2, 0))
        
        ttk.Label(template_actions, text="Use {prompt} where your input should be inserted", font=("", 8)).pack(side=tk.LEFT)
        ttk.Button(template_actions, text="Save Template", command=self.save_prompt_template).pack(side=tk.RIGHT)
          # Prompt input
        prompt_frame = ttk.Frame(chat_frame)
        prompt_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(prompt_frame, text="Prompt:").pack(anchor=tk.W)
        self.prompt_entry = tk.Text(prompt_frame, height=1, wrap=tk.WORD)
        self.prompt_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(chat_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.generate_btn = ttk.Button(button_frame, text="Generate New", command=self.generate_image)
        self.generate_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.modify_btn = ttk.Button(button_frame, text="Modify Current", command=self.modify_image)
        self.modify_btn.pack(fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(chat_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
    
    def create_tools_section(self, parent):
        """Create the tools section"""
        tools_frame = ttk.LabelFrame(parent, text="Image Tools", padding="10")
        tools_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Tool buttons
        tool_buttons = ttk.Frame(tools_frame)
        tool_buttons.pack(fill=tk.X)
        # Undo button
        ttk.Button(tool_buttons, text="Undo", command=self.undo_edit).pack(side=tk.LEFT, padx=(0, 5))
        # Other editing tools
        ttk.Button(tool_buttons, text="More Pixelated", command=self.apply_more_pixelation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tool_buttons, text="Less Pixelated", command=self.apply_less_pixelation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tool_buttons, text="Remove Background", command=self.remove_background).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tool_buttons, text="Increase Contrast", command=self.increase_contrast).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tool_buttons, text="Increase Brightness", command=self.increase_brightness).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tool_buttons, text="Resize Image", command=self.resize_image).pack(side=tk.LEFT)
        
        # Checkbox for automatic background removal
        ttk.Checkbutton(tools_frame, text="Auto Remove Background", variable=self.auto_remove_bg).pack(anchor=tk.W, pady=(10, 0))
    
    def initialize_generator(self):
        """Initialize the image generator"""
        try:
            self.image_generator = ImageGenerator()
            self.status_var.set("AI Generator initialized successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize AI generator: {str(e)}")
            self.status_var.set("Error: AI Generator not available")
    
    def add_to_chat(self, message, sender="System"):
        """Add message to chat history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_history.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_history.see(tk.END)
    
    def get_prompt(self):
        """Get prompt from entry widget"""
        base_prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if base_prompt: 
            # Get the template and replace {prompt} placeholder with user input
            template = self.prompt_template.get("1.0", tk.END).strip()
            enhanced_prompt = template.replace("{prompt}", base_prompt)
            return enhanced_prompt
        return base_prompt
    
    def clear_prompt(self):
        """Clear the prompt entry"""
        self.prompt_entry.delete("1.0", tk.END)
    
    def display_image(self, image):
        """Display image on canvas"""
        if image:
            # Resize image to fit canvas if needed
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                display_image = image.copy()
                display_image.thumbnail((canvas_width - 20, canvas_height - 20), Image.NEAREST)
                
                self.current_photo = ImageTk.PhotoImage(display_image)
                self.canvas.delete("all")
                self.canvas.create_image(
                    canvas_width // 2, 
                    canvas_height // 2, 
                    anchor=tk.CENTER, 
                    image=self.current_photo
                )
                
                self.current_image = image
    
    def generate_image(self):
        """Generate new image from prompt"""
        prompt = self.get_prompt()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt")
            return
        
        if not self.image_generator:
            messagebox.showerror("Error", "AI Generator not available")
            return
        
        self.add_to_chat(f"Generating: {prompt}", "User")
        self.generate_btn.configure(state='disabled')
        self.progress.start()
        self.status_var.set("Generating image...")
        
        def generate_thread():
            try:
                image = self.image_generator.generate_image(prompt)
                self.root.after(0, lambda: self.on_generation_complete(image, "Image generated successfully!"))
            except Exception as e:
                self.root.after(0, lambda: self.on_generation_error(str(e)))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def modify_image(self):
        """Modify current image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to modify. Generate an image first.")
            return
        
        prompt = self.get_prompt()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a modification prompt")
            return
        
        self.add_to_chat(f"Modifying with: {prompt}", "User")
        self.modify_btn.configure(state='disabled')
        self.progress.start()
        self.status_var.set("Modifying image...")
        
        def modify_thread():
            try:
                image = self.image_generator.modify_image(self.current_image, prompt)
                self.root.after(0, lambda: self.on_generation_complete(image, "Image modified successfully!"))
            except Exception as e:
                self.root.after(0, lambda: self.on_generation_error(str(e)))
        
        threading.Thread(target=modify_thread, daemon=True).start()
    
    def on_generation_complete(self, image, message):
        """Handle successful image generation"""
        # Automatically remove background from generated images if enabled
        if self.auto_remove_bg.get():
            image = ImageProcessor.remove_background(image)
        
        self.display_image(image)
        self.add_to_chat(message, "System")
        self.clear_prompt()
        self.generate_btn.configure(state='normal')
        self.modify_btn.configure(state='normal')
        self.progress.stop()
        self.status_var.set("Ready")
    
    def on_generation_error(self, error_message):
        """Handle image generation error"""
        self.add_to_chat(f"Error: {error_message}", "System")
        messagebox.showerror("Generation Error", error_message)
        self.generate_btn.configure(state='normal')
        self.modify_btn.configure(state='normal')
        self.progress.stop()
        self.status_var.set("Error occurred")
    
    def save_image(self):
        """Save current image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            initialdir=self.output_dir
        )
        
        if filename:
            if ImageProcessor.save_image(self.current_image, filename):
                self.add_to_chat(f"Image saved to: {filename}", "System")
                self.status_var.set("Image saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save image")
    
    def load_image(self):
        """Load image from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        
        if filename:
            image = ImageProcessor.load_image(filename)
            if image:
                self.display_image(image)
                self.add_to_chat(f"Image loaded from: {filename}", "System")
                self.status_var.set("Image loaded successfully")
            else:
                messagebox.showerror("Error", "Failed to load image")
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")
        self.current_image = None
        self.current_photo = None
        self.add_to_chat("Canvas cleared", "System")
        self.status_var.set("Canvas cleared")
    
    def apply_more_pixelation(self):
        """Apply more pixelation to current image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to pixelate")
            return
        
        # save state for undo
        self.edit_history.append(self.current_image.copy())
        pixelated = ImageProcessor.pixelate(self.current_image, pixel_size=12)
        self.display_image(pixelated)
        self.add_to_chat("Applied more pixelation", "System")
    
    def apply_less_pixelation(self):
        """Apply less pixelation to current image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to pixelate")
            return
        
        # save state for undo
        self.edit_history.append(self.current_image.copy())
        pixelated = ImageProcessor.pixelate(self.current_image, pixel_size=4)
        self.display_image(pixelated)
        self.add_to_chat("Applied less pixelation", "System")
    
    def copy_to_clipboard(self):
        """Copy current image to clipboard as DIB for Windows"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to copy")
            return
        # Convert image to DIB format
        output = BytesIO()
        bmp = self.current_image.convert('RGB')
        bmp.save(output, format='BMP')
        data = output.getvalue()[14:]
        # Set clipboard data
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)
            win32clipboard.CloseClipboard()
            self.add_to_chat("Image copied to clipboard", "System")
            self.status_var.set("Copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")
    
    def increase_contrast(self):
        """Increase image contrast"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to modify")
            return
        
        # save state for undo
        self.edit_history.append(self.current_image.copy())
        enhanced = ImageProcessor.adjust_contrast(self.current_image, 1.3)
        self.display_image(enhanced)
        self.add_to_chat("Increased contrast", "System")
    
    def increase_brightness(self):
        """Increase image brightness"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to modify")
            return
        
        # save state for undo
        self.edit_history.append(self.current_image.copy())
        enhanced = ImageProcessor.adjust_brightness(self.current_image, 1.2)
        self.display_image(enhanced)
        self.add_to_chat("Increased brightness", "System")
    
    def resize_image(self):
        """Resize current image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to resize")
            return
        
        # Simple resize dialog
        new_size = simpledialog.askstring("Resize", "Enter new size (width,height):", initialvalue="512,512")
        if new_size:
            try:
                width, height = map(int, new_size.split(','))
                # save state for undo
                self.edit_history.append(self.current_image.copy())
                resized = ImageProcessor.resize_image(self.current_image, (width, height), maintain_aspect=False)
                self.display_image(resized)
                self.add_to_chat(f"Resized to {width}x{height}", "System")
            except ValueError:
                messagebox.showerror("Error", "Invalid size format. Use 'width,height'")
    
    def remove_background(self):
        """Remove background from current image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to process")
            return
        
        # save state for undo
        self.edit_history.append(self.current_image.copy())
        # Use the background removal method from ImageProcessor
        processed = ImageProcessor.remove_background(self.current_image)
        self.display_image(processed)
        self.add_to_chat("Background removed", "System")

    def undo_edit(self):
        """Undo the last image edit"""
        if not self.edit_history:
            messagebox.showinfo("Info", "Nothing to undo")
            return
        previous = self.edit_history.pop()
        self.display_image(previous)
        self.add_to_chat("Undo edit", "System")
        self.status_var.set("Undo performed")

    def load_prompt_template(self):
        """Load the prompt template from file if it exists"""
        try:
            if os.path.exists(self.template_file):
                with open(self.template_file, 'r') as file:
                    template_text = file.read().strip()
                    if template_text:
                        return template_text
            return self.default_template_text
        except Exception as e:
            self.add_to_chat(f"Error loading template: {str(e)}", "System")
            return self.default_template_text
    
    def save_prompt_template(self, template_text=None):
        """Save the current prompt template to file"""
        if template_text is None:
            template_text = self.prompt_template.get("1.0", tk.END).strip()
        
        try:
            with open(self.template_file, 'w') as file:
                file.write(template_text)
            self.add_to_chat("Prompt template saved to file", "System")
            self.status_var.set("Template saved")
            return True
        except Exception as e:
            self.add_to_chat(f"Error saving template: {str(e)}", "System")
            self.status_var.set("Error saving template")
            return False

def main():
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
