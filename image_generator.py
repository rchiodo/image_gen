"""
Image generation module using OpenAI's DALL-E API
"""

import os
import requests
from io import BytesIO
from PIL import Image
import openai
from dotenv import load_dotenv

load_dotenv()



class ImageGenerator:
    def __init__(self):
        # You will need to set these environment variables or edit the following values.
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rchio-mb1ft4rz-eastus.cognitiveservices.azure.com/")
        api_version = os.getenv("OPENAI_API_VERSION", "2024-04-01-preview")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        self.client = openai.AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
    
   
    def generate_image(self, prompt, size="1024x1024"):
        """Generate a new pixelated image from prompt"""
        try:
           
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download the image
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            
            # Apply additional pixelation effect
            image = self.apply_pixelation(image)
            # Remove background (white) to transparent
            image = self.make_background_transparent(image)
            return image
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")
    
    def modify_image(self, current_image, prompt, size="1024x1024"):
        """Modify existing image based on prompt (simulate with new generation)"""
        # Note: DALL-E 3 doesn't support image editing, so we'll generate a new image
        # with a modified prompt that includes context about the current image
        modify_prompt = f"Modify this concept: {prompt}, pixel art style, 8-bit, pixelated"
        return self.generate_image(modify_prompt, size)
    
    def apply_pixelation(self, image, pixel_size=8):
        """Apply pixelation effect to an image"""
        # Get original size
        original_size = image.size
        
        # Resize down
        small_size = (original_size[0] // pixel_size, original_size[1] // pixel_size)
        small_image = image.resize(small_size, Image.NEAREST)
        
        # Resize back up
        pixelated_image = small_image.resize(original_size, Image.NEAREST)
        
        return pixelated_image
    
    def make_background_transparent(self, image, threshold=250):
        """Make white (or near-white) background transparent"""
        # Ensure image has alpha channel
        img = image.convert("RGBA")
        datas = img.getdata()
        new_data = []
        for item in datas:
            r, g, b, a = item
            # Treat near-white as background
            if r >= threshold and g >= threshold and b >= threshold:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        return img
