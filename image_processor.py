"""
Image processing utilities
"""

from PIL import Image, ImageFilter, ImageEnhance
import os
from rembg import remove
import io

class ImageProcessor:
    @staticmethod
    def pixelate(image, pixel_size=8):
        """Apply pixelation effect"""
        original_size = image.size
        small_size = (original_size[0] // pixel_size, original_size[1] // pixel_size)
        small_image = image.resize(small_size, Image.NEAREST)
        return small_image.resize(original_size, Image.NEAREST)
    
    @staticmethod
    def resize_image(image, new_size, maintain_aspect=True):
        """Resize image while maintaining pixelated style"""
        if maintain_aspect:
            image.thumbnail(new_size, Image.NEAREST)
            return image
        else:
            return image.resize(new_size, Image.NEAREST)
    
    @staticmethod
    def adjust_contrast(image, factor=1.2):
        """Adjust image contrast"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_brightness(image, factor=1.1):
        """Adjust image brightness"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def save_image(image, filepath):
        """Save image to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            image.save(filepath)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    @staticmethod
    def load_image(filepath):
        """Load image from file"""
        try:
            return Image.open(filepath)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    @staticmethod
    def remove_background(image: Image.Image) -> Image.Image:
        """Remove background using rembg with alpha‐matting tuned to preserve interior colors."""
        buf_in = io.BytesIO()
        image.save(buf_in, format="PNG")
        img_bytes = buf_in.getvalue()

        # Enable alpha matting and lower the foreground threshold so internal pixels aren't dropped
        result_bytes = remove(
            img_bytes,
            alpha_matting=True,
            alpha_matting_foreground_threshold=200,   # lower = more pixels kept
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=3
        )

        buf_out = io.BytesIO(result_bytes)
        return Image.open(buf_out).convert("RGBA")
