"""
Image processing utilities
"""

from PIL import Image, ImageFilter, ImageEnhance
import os
from rembg import remove
from io import BytesIO

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
    def remove_background(image):
        """Remove background using rembg"""
        # Ensure RGBA
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        # Convert to bytes
        buf = BytesIO()
        image.save(buf, format='PNG')
        img_bytes = buf.getvalue()
        # Call rembg
        result_bytes = remove(img_bytes)
        # Load back to PIL Image
        new_image = Image.open(BytesIO(result_bytes)).convert('RGBA')
        return new_image
